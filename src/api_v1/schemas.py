from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Optional
from src.utils.validation import DriverValidator, VehicleValidator, OrdersInfoValidator, KeyValidator


class StrictBaseModel(BaseModel):
    class Config:
        extra = "forbid"


class Driver(StrictBaseModel):
    user_agree: bool
    name: str = Field(..., min_length=2, max_length=25)
    surname: str = Field(..., min_length=2, max_length=50)
    middle_name: str = Field("", max_length=25)
    number: str = Field(..., min_length=10, max_length=15)
    passport_series: Optional[str] = Field(None, min_length=1, max_length=4)
    passport_number: str = Field(..., min_length=6, max_length=9)

    @field_validator("user_agree")
    def check_user_agree(cls, value):
        if value is not True:
            raise ValueError("Поле 'user_agree' должно быть равно True")
        return value

    @field_validator("name")
    def validate_name(cls, value):
        if not DriverValidator.validate_name(value):
            raise ValueError("Имя должно содержать только кириллицу и быть длиной от 2 до 25 символов")
        return value

    @field_validator("surname")
    def validate_surname(cls, value):
        if not DriverValidator.validate_surname(value):
            raise ValueError(
                "Фамилия должна содержать только кириллицу, быть длиной от 2 до 25 символов, "
                "и может содержать тире для двойной фамилии (дополнительно от 2 до 24 символов)"
            )
        return value

    @field_validator("middle_name")
    def validate_middle_name(cls, value):
        if not DriverValidator.validate_middle_name(value):
            raise ValueError("Отчество должно быть пустой строкой или содержать кириллицу длиной от 2 до 25 символов")
        return value

    @field_validator("number")
    def validate_number(cls, value):
        if not DriverValidator.validate_phone_number(value):
            raise ValueError(
                "Номер телефона должен соответствовать российскому формату: "
                "+79111234567, 89111234567, +7 911 123-45-67, 8 (911) 123-45-67, 9111234567."
            )
        return DriverValidator.format_phone_number(value)

    @field_validator("passport_series")
    def validate_passport_series(cls, value):
        if not DriverValidator.validate_passport_series(value):
            raise ValueError(
                "Серия паспорта должна соответствовать формату ввода"
            )
        return value

    @field_validator("passport_number")
    def validate_passport_number(cls, value):
        if not DriverValidator.validate_passport_number(value):
            raise ValueError(
                "Номер паспорта должен соответствовать формату ввода"
            )
        return value

    @model_validator(mode="after")
    def check_full_passport(self):
        """
        Проверяет, что введенные паспортные данные относятся к одному и тому же формату ввода
        """
        if not DriverValidator.validate_full_passport(self.passport_series, self.passport_number):
            raise ValueError("Паспортные не относятся к единому формату ввода")
        return self


class VehicleInfo(StrictBaseModel):
    vehicle_number: str = Field(..., min_length=6, max_length=9)
    has_trailer: bool
    trailer_number: Optional[str] = Field(None, min_length=3, max_length=10)
    vehicle_weight: bool

    @field_validator("vehicle_number")
    def validate_vehicle_number(cls, value):
        if not VehicleValidator.validate_vehicle_number(value):
            raise ValueError(
                "Номер ТС должен соответствовать формату ввода"
            )
        return value

    @field_validator("has_trailer")
    def check_has_trailer(cls, value):
        if not isinstance(value, bool):
            raise ValueError("Поле 'has_trailer' должно иметь булево значение")
        return value

    @field_validator("trailer_number")
    def validate_trailer_number(cls, value):
        if value is not None and value != "" and not VehicleValidator.validate_trailer_number(value):
            raise ValueError("Номер прицепа не соответствует формату ввода")
        return value

    @field_validator("vehicle_weight")
    def check_vehicle_weight(cls, value):
        if not isinstance(value, bool):
            raise ValueError("Поле 'vehicle_weight' должно иметь булево значение")
        return value

    @model_validator(mode="after")
    def check_trailer_consistency(self):
        """
        Проверяет, что если has_trailer = False, то trailer_number должен быть None.
        Если has_trailer = True, то trailer_number должен присутствовать и быть корректным.
        """
        if self.has_trailer:
            if self.trailer_number is None:
                raise ValueError("Поле 'trailer_number' должно быть заполнено, если 'has_trailer' = true")
        else:
            if self.trailer_number is not None:
                raise ValueError("Поле 'trailer_number' должно быть null, если 'has_trailer' = false")
        return self


class PayloadItem(StrictBaseModel):
    Number: str
    Status: Optional[bool]

    @field_validator("Number")
    def validate_order_number(cls, value):
        if not OrdersInfoValidator.validate_order(value):
            raise ValueError(
                "Номер заявки должен соответствовать формату ввода"
            )
        return value


class IncomingData(StrictBaseModel):
    type: str
    driver: Driver
    contact_point: str
    job_type: str
    use_orders: Optional[bool]
    payload: List[PayloadItem]
    partners: str
    vehicle_info: VehicleInfo

    @field_validator("type")
    def validate_type(cls, value):
        if value != OrdersInfoValidator.request_type():
            raise ValueError("Поле 'type' должно быть равно 'Внешняя регистрация'")
        return value

    @field_validator("contact_point")
    def validate_contact_point(cls, value):
        allowed_values = OrdersInfoValidator.allowed_contact_points()
        if value not in allowed_values:
            raise ValueError(f"Поле 'contact_point' должно быть одним из: {', '.join(allowed_values)}")
        return value

    @field_validator("job_type")
    def validate_job_type(cls, value):
        allowed_values = OrdersInfoValidator.allowed_job_type()
        if value not in allowed_values:
            raise ValueError(f"Поле 'job_type' должно быть одним из: {', '.join(allowed_values)}")
        return value

    @field_validator("partners")
    def validate_order_number(cls, value):
        if not OrdersInfoValidator.validate_partner(value):
            raise ValueError("Название контрагента должно соответствовать формату ввода")
        return value

    @model_validator(mode="after")
    def check_payload_not_empty(self):
        """
        Проверяет, что список payload не пустой.
        """
        # Если payload пустой, выбрасываем ошибку
        if not self.payload:
            raise ValueError("Список заявок не должен быть пустым")
        return self


class PurgeKeyData(StrictBaseModel):
    type: str
    key: str

    @field_validator("type")
    def validate_type(cls, value):
        if value != KeyValidator.request_type():
            raise ValueError("Поле 'type' должно быть равно 'Запрос на аннулирование'")
        return value

    @field_validator("key")
    def validate_key(cls, value):
        if not KeyValidator.validate_key(value):
            raise ValueError("Поле 'key' должно состоять из шести чисел")
        return value
