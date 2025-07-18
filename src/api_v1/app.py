import logging
import asyncio
import uvicorn
from pydantic import ValidationError
from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.schemas import IncomingData, PurgeKeyData
from src.api_v1.db_session import get_db_session
from src.api_v1.pallet_schemas import OrderRequest
from src.api_v1.calc_pallet import process_pallet

from src.bot.handlers.qr_code import generate_api_v1_key
from src.database.scripts.admin import add_fast_reg_vehicle, remove_fast_reg_vehicle, order_reset_key, vehicle_reset_key
from src.database.scripts.api_v1 import outer_reg_add_user, outer_reg_delete_user
from src.database.scripts.orders import add_fast_reg_orders, remove_fast_reg_orders
from src.services.api_service import api_service
from src.services.settings import settings


logger = logging.getLogger("backend")

app = FastAPI()

security = HTTPBasic()

# app.add_middleware(HTTPSRedirectMiddleware)

app.add_middleware(
    CORSMiddleware,                  # Настройка CORS
    allow_origins=["*"],             # Разрешить запросы с любого домена
    allow_methods=["POST"],          # Разрешить только POST-запросы
    allow_headers=["Content-Type"],  # Разрешить только заголовки Content-Type
)


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != settings.app.get("username") or credentials.password != settings.app.get("password"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True


@app.post("/api/v1/registration")
async def registration_handler(request: Request,
                               authenticated: bool = Depends(authenticate),
                               session: AsyncSession = Depends(get_db_session)):
    if request.headers.get("Content-Type") != "application/json":
        raise HTTPException(status_code=400, detail="Only JSON requests are allowed")

    if not await request.body():
        raise HTTPException(status_code=400, detail="Request body is empty")
    try:
        try:
            raw_data = await request.json()
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid JSON format")
        logger.info(f"Requested raw data: {raw_data}")
        validated_data = IncomingData(**raw_data)
        response_data = validated_data.model_dump()
        logger.info(f"Pydantic validation data: {validated_data}")

        # Подготавливаем данные для отправки на другую API
        api_request_data = {
            "contact_point": validated_data.contact_point,
            "job_type": validated_data.job_type,
            "use_orders": validated_data.use_orders,
            "orders": [item.dict() for item in validated_data.payload],  # Преобразуем payload в список словарей
            "partner": validated_data.partners,
        }

        logger.info(f"Send info to inner api: {api_request_data}")
        api_response = await api_service.send_orders_to_api(api_request_data)
        logger.info(f"Request from inner api: {api_response}")
        if not api_response:
            logger.error(f"No response from inner api")
            raise HTTPException(status_code=500, detail="Ошибка при отправке данных в сервис проверки заявок")

        if api_response.get("is_error"):
            errors = api_response.get("error", [])
            error_msg = ", ".join(errors) if errors else "Неизвестная ошибка в сервисе проверки заявок"
            response_data.update({"is_error": True, "message": error_msg})
            logger.info(f"Response get with error in inner api: {response_data}")
            return JSONResponse(content=response_data, status_code=200)

        updated_payload = []
        error_orders = []

        for order in api_response.get("payload", []):
            number = order.get("Number")
            status = order.get("Status")
            updated_payload.append({"Number": number, "Status": status, "row_number": None})

            if status is False:
                error_orders.append(number)

        if error_orders:
            error_message = f"Не найдена заявка: {', '.join(error_orders)}"
            response_data.update({
                "is_error": True,
                "message": error_message,
                "payload": updated_payload,
                "use_orders": api_response.get("use_orders"),
            })
            logger.info(f"Response get with false status orders: {response_data}")
            return JSONResponse(content=response_data, status_code=200)

        full_data = {
            "name": validated_data.driver.name,
            "surname": validated_data.driver.surname,
            "middle_name": validated_data.driver.middle_name,
            "number": validated_data.driver.number,
            "licence_series": validated_data.driver.passport_series
            if validated_data.driver.passport_series is not None
            else "",
            "licence_number": validated_data.driver.passport_number,
            "contact_point": validated_data.contact_point,
            "job_type": validated_data.job_type,
            "use_orders": api_response.get("use_orders"),
            "orders": updated_payload,
            "partner": validated_data.partners,
            "vehicle_number": validated_data.vehicle_info.vehicle_number,
            "trailer": validated_data.vehicle_info.has_trailer,
            "trailer_number": validated_data.vehicle_info.trailer_number
            if validated_data.vehicle_info.trailer_number is not None
            else "",
            "trailer_weight": validated_data.vehicle_info.vehicle_weight,
        }
        logger.info(f"Collected full data {full_data}")
        is_new_user = False
        try:
            is_new_user = await outer_reg_add_user(session, full_data)
            await add_fast_reg_orders(session, full_data)
            await add_fast_reg_vehicle(session, full_data)
            logger.info(f"Completely add data to db with new user status: {is_new_user}")
        except Exception as ex:
            logger.error(f"Ошибка записи данных в базу данных: {ex}", exc_info=True)
            if is_new_user:
                await outer_reg_delete_user(session, full_data)
            await remove_fast_reg_orders(session, full_data)
            await remove_fast_reg_vehicle(session, full_data)
            raise HTTPException(status_code=500, detail="Ошибка записи данных в базу данных")

        key = await generate_api_v1_key(session, full_data)
        logger.info(f"Generated activation key: {key}")
        if not key:
            raise HTTPException(status_code=500, detail="Не удалось сгенерировать ключ активации")

        # Если все успешно, обновляем данные и возвращаем ответ
        response_data.update({
            "use_orders": api_response.get("use_orders"),
            "payload": updated_payload,
            "key": key,
            "qr": None,
            "is_error": False,
            "message": "Успешная регистрация"
        })
        logger.info(f"Successful registration with data: {response_data}")
        return JSONResponse(content=response_data, status_code=200)
    except ValidationError as ve:
        # Перехватываем ошибки валидации
        error_details = ve.errors()
        first_error = error_details[0]
        field_name = first_error.get("loc", "Неизвестное поле")
        field_name = field_name[-1] if len(field_name) != 0 else "Неизвестное поле"
        error_msg = first_error.get("msg", "Непредвиденная ошибка")

        logger.error(f"Validation error {field_name}: {error_msg}")

        # Формируем ответ с полным пакетом данных и информацией об ошибке
        raw_data = await request.json()
        return JSONResponse(
            status_code=422,
            content={
                **raw_data,
                "is_error": True,
                "message": f"Ошибка валидации поля '{field_name}': {error_msg}"
            }
        )


@app.post("/api/v1/purge_key")
async def purge_key_handler(request: Request,
                            authenticated: bool = Depends(authenticate),
                            session: AsyncSession = Depends(get_db_session)):
    if request.headers.get("Content-Type") != "application/json":
        raise HTTPException(status_code=400, detail="Only JSON requests are allowed")

    if not await request.body():
        raise HTTPException(status_code=400, detail="Request body is empty")
    try:
        try:
            raw_data = await request.json()
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid JSON format")
        logger.info(f"Requested raw data: {raw_data}")
        validated_data = PurgeKeyData(**raw_data)
        response_data = validated_data.model_dump()
        logger.info(f"Pydantic validation data: {validated_data}")

        key = validated_data.key
        if await order_reset_key(session, key) is not None and await vehicle_reset_key(session, key) is not None:
            response_data.update({
                "is_error": False,
                "message": f"Код ${key} успешно аннулирован"
            })
        else:
            response_data.update({
                "is_error": True,
                "message": f"Код ${key} не найден или уже не может быть аннулирован"
            })

        return JSONResponse(content=response_data, status_code=200)

    except ValidationError as ve:
        # Перехватываем ошибки валидации
        error_details = ve.errors()
        first_error = error_details[0]
        field_name = first_error.get("loc", "Неизвестное поле")
        field_name = field_name[-1] if len(field_name) != 0 else "Неизвестное поле"
        error_msg = first_error.get("msg", "Непредвиденная ошибка")

        logger.error(f"Validation error {field_name}: {error_msg}")

        # Формируем ответ с полным пакетом данных и информацией об ошибке
        raw_data = await request.json()
        return JSONResponse(
            status_code=422,
            content={
                **raw_data,
                "is_error": True,
                "message": f"Ошибка валидации поля '{field_name}': {error_msg}"
            }
        )
    except Exception as ex:
        logger.error(f"Ошибка аннулирования кода: {ex}")
        raise HTTPException(status_code=500, detail="Возникла ошибка с аннулированием кода. Попробуйте ещё раз")


@app.post("/api/v2/calculate-pallets")
async def calculate_pallets(request: OrderRequest):
    try:
        result = process_pallet(
            order_number=request.номер_заказа,
            items_data=request.позиции,
            weight_limit=request.допустимый_вес,
            volume_limit=request.допустимый_объем
        )
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.api_route("/{path:path}", methods=["GET", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
async def handle_invalid_methods(authenticated: bool = Depends(authenticate)):
    return JSONResponse(
        status_code=405,
        content={"is_error": True, "message": "Only POST requests are allowed"}
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Catch an exception in backend: {exc}")
    try:
        raw_data = await request.json()
    except Exception as ex:
        logger.error(f"Cannot make raw data: {ex}")
        raw_data = {}
    return JSONResponse(
        status_code=500,
        content={
            **raw_data,
            "is_error": True,
            "message": f"Произошла ошибка на стороне сервера: {str(exc)}"
        }
    )

if __name__ == "__main__":
    import os
    from pytz import timezone
    from datetime import datetime
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Устанавливаем московское время через pytz
    moscow_tz = timezone('Europe/Moscow')
    logging.Formatter.converter = lambda *args: datetime.now(moscow_tz).timetuple()

    fastapi_log_file = os.path.join("../../logs", "fastapi.log")
    fastapi_handler = logging.FileHandler(fastapi_log_file, mode="a", encoding="utf-8")
    fastapi_handler.setFormatter(formatter)
    fastapi_logger = logging.getLogger("backend")
    fastapi_logger.setLevel(logging.DEBUG)
    fastapi_logger.addHandler(fastapi_handler)

    async def run_fastapi(reload=False):
        config = uvicorn.Config(
            app,
            host="0.0.0.0",
            port=443,
            log_level="info",
            reload=reload,  # Включаем только для разработки
            ssl_keyfile="/etc/ssl/my_domain/private.key",
            ssl_certfile="/etc/ssl/my_domain/certificate.crt"
        )
        server = uvicorn.Server(config)
        await server.serve()


    asyncio.run(run_fastapi(True))
