from pydantic import BaseModel
from typing import List, Optional


# Входные данные
class OrderItem(BaseModel):
    Артикул: str
    Номенклатура: Optional[str] = None
    Количество: float
    Маркер: Optional[str] = None
    Масса: float
    Объем: float


class OrderRequest(BaseModel):
    номер_заказа: str
    допустимый_вес: Optional[float] = 550.0  # кг
    допустимый_объем: Optional[float] = 1.8  # м³
    позиции: List[OrderItem]


# Выходные данные
class PackedItem(BaseModel):
    Артикул: str
    Номенклатура: Optional[str] = None
    Количество: float
    Маркер: Optional[str] = None
    Вес: float
    Объем: float


class PackedPallet(BaseModel):
    номер_паллета: str
    Итого: dict
    Товары: List[PackedItem]


class PalletResponse(BaseModel):
    result: List[PackedPallet]
