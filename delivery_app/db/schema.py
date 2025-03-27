from pydantic import BaseModel, EmailStr
from typing import Optional
from delivery_app.db.models import StarChoices, OrderStatusChoices, CourierStatus, StatusChoices
from datetime import datetime


class UserProfileSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str
    email: EmailStr
    phone_number: Optional[str]
    profile_image: Optional[str]
    age: Optional[int]
    status: StatusChoices
    date_registered: datetime

    class Config:
        from_attributes = True


class CategorySchema(BaseModel):
    category_name: str

    class Config:
        from_attributes = True


class StoreSchema(BaseModel):
    store_name: str
    category_id: int
    description: str
    store_image: str
    address: str
    owner_id: int

    class Config:
        from_attributes = True


class ContactSchema(BaseModel):
    title: str
    contact_number: Optional[str]
    social_network: Optional[str]
    store_id: int

    class Config:
        from_attributes = True


class ProductSchema(BaseModel):
    product_name: str
    description: str
    product_image: str
    price: float
    store_id: int

    class Config:
        from_attributes = True


class ComboSchema(BaseModel):
    combo_name: str
    description: str
    price: float
    store_id: int

    class Config:
        from_attributes = True


class OrderSchema(BaseModel):
    client_id: int
    order_status: OrderStatusChoices
    delivery_address: str
    courier_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CourierSchema(BaseModel):
    courier_id: int
    order_id: int
    courier_status: CourierStatus

    class Config:
        from_attributes = True


class StoreReviewSchema(BaseModel):
    client_id: int
    store_id: int
    text: str
    star: StarChoices
    created_date: datetime

    class Config:
        from_attributes = True


class CourierReviewSchema(BaseModel):
    client_id: int
    courier_id: int
    star: StarChoices
    created_date: datetime

    class Config:
        from_attributes = True

