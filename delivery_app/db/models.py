from delivery_app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Enum, DateTime, ForeignKey, Text, DECIMAL
from typing import Optional, List
from enum import Enum as PyEnum
from datetime import datetime
from passlib.hash import bcrypt


class StatusChoices(str, PyEnum):
    client = 'client'
    owner = 'owner'
    courier = 'courier'


class OrderStatusChoices(str, PyEnum):
    waiting_for_processing = 'waiting for processing'
    delivering = 'delivering'
    delivered = 'delivered'
    canceled = 'canceled'


class CourierStatus(str, PyEnum):
    free = 'free'
    busy = 'busy'


class StarChoices(int, PyEnum):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5


class UserProfile(Base):
    __tablename__ = 'user_profile'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[str] = mapped_column(String(32))
    username: Mapped[str] = mapped_column(String, unique=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    profile_image: Mapped[str | None] = mapped_column(String, nullable=True)
    age: Mapped[int or None] = mapped_column(Integer, nullable=True)
    status: Mapped[StatusChoices] = mapped_column(Enum(StatusChoices), default=StatusChoices.client.value)
    date_registered: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_store: Mapped[List['Store']] = relationship('Store', back_populates='owner',
                                                     cascade='all, delete-orphan')
    orders: Mapped[List['Order']] = relationship('Order', back_populates='client', foreign_keys='Order.client_id',
                                                 cascade='all, delete-orphan')
    deliveries: Mapped[List['Order']] = relationship('Order', back_populates='courier', foreign_keys='Order.courier_id',
                                                     cascade='all, delete-orphan')
    user_courier: Mapped[List['Courier']] = relationship('Courier', back_populates='courier',
                                                         foreign_keys='Courier.courier_id',
                                                         cascade='all, delete-orphan')
    store_reviews: Mapped[List['StoreReview']] = relationship('StoreReview', back_populates='client',
                                                              foreign_keys='StoreReview.client_id',
                                                              cascade='all, delete-orphan')
    reviews_courier: Mapped[List['CourierReview']] = relationship('CourierReview', back_populates='client',
                                                                  foreign_keys='CourierReview.client_id',
                                                                  cascade='all, delete-orphan')
    user_tokens: Mapped[List['RefreshToken']] = relationship('RefreshToken', back_populates='user',
                                                             cascade='all, delete-orphan')

    def set_passwords(self, password: str):
        self.hashed_password = bcrypt.hash(password)

    def check_password(self, password: str):
        return bcrypt.verify(password, self.hashed_password)

    def __repr__(self):
        return f'{self.first_name} - {self.last_name}'


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    token: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='user_tokens')


    def __repr__(self):
        return f'{self.user_id}'


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_name: Mapped[str] = mapped_column(String(32), unique=True)
    category_store: Mapped[List['Store']] = relationship(back_populates='category',
                                                         cascade='all, delete-orphan')


    def __repr__(self):
        return f'{self.category_name}'


class Store(Base):
    __tablename__ = 'store'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    store_name: Mapped[str] = mapped_column(String(32))
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    category: Mapped['Category'] = relationship('Category', back_populates='category_store')
    description: Mapped[str] = mapped_column(Text)
    store_image: Mapped[str] = mapped_column(String)
    address: Mapped[str] = mapped_column(String(64))
    owner_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    owner: Mapped['UserProfile'] = relationship('UserProfile', back_populates='user_store')
    store_contact: Mapped[List['Contact']] = relationship('Contact', back_populates='store',
                                                          cascade='all, delete-orphan')
    products_store: Mapped[List['Product']] = relationship('Product', back_populates='store_product',
                                                           cascade='all, delete-orphan')
    store_comba: Mapped[List['Combo']] = relationship('Combo', back_populates='store',
                                                      cascade='all, delete-orphan')
    store_reviews: Mapped[List['StoreReview']] = relationship('StoreReview', back_populates='store',
                                                              foreign_keys='StoreReview.store_id',
                                                              cascade='all, delete-orphan')

    def __str__(self):
        return f'{self.store_name}'


class Contact(Base):
    __tablename__ = 'contact'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(64))
    contact_number: Mapped[str or None] = mapped_column(String(32), nullable=True)
    social_network: Mapped[str or None] = mapped_column(String, nullable=True)
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    store: Mapped['Store'] = relationship('Store', back_populates='store_contact')


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(Text)
    product_image: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    store_product: Mapped['Store'] = relationship('Store', back_populates='products_store')


class Combo(Base):
    __tablename__ = 'combo'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    combo_name: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    store: Mapped['Store'] = relationship('Store', back_populates='store_comba')


class Order(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    client: Mapped['UserProfile'] = relationship('UserProfile', back_populates='orders', foreign_keys=[client_id])
    orders_courier: Mapped[List['Courier']] = relationship('Courier', back_populates='order',
                                                           foreign_keys='Courier.order_id',
                                                           cascade='all, delete-orphan')
    order_status: Mapped[OrderStatusChoices] = mapped_column(Enum(OrderStatusChoices),
                                                             default=OrderStatusChoices.waiting_for_processing.value)
    delivery_address: Mapped[str] = mapped_column(String(128))
    courier_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    courier: Mapped['UserProfile'] = relationship('UserProfile', back_populates='deliveries', foreign_keys=[courier_id])
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Courier(Base):
    __tablename__ = 'courier'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    courier_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    courier: Mapped['UserProfile'] = relationship('UserProfile', back_populates='user_courier',
                                                  foreign_keys=[courier_id])
    order_id: Mapped[int | None] = mapped_column(ForeignKey('order.id'), nullable=True)
    order: Mapped['Order'] = relationship('Order', back_populates='orders_courier', foreign_keys=[order_id])
    courier_status: Mapped[CourierStatus] = mapped_column(Enum(CourierStatus), default=CourierStatus.free.value)
    courier_reviews: Mapped[List['CourierReview']] = relationship('CourierReview', back_populates='courier',
                                                                  foreign_keys='CourierReview.courier_id',
                                                                  cascade='all, delete-orphan')


class StoreReview(Base):
    __tablename__ = 'store_review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    client: Mapped['UserProfile'] = relationship('UserProfile', back_populates='store_reviews',
                                                 foreign_keys=[client_id])
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    store: Mapped['Store'] = relationship('Store', back_populates='store_reviews', foreign_keys=[store_id])
    text: Mapped[str] = mapped_column(Text)
    star: Mapped[StarChoices] = mapped_column(Enum(StarChoices))
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class CourierReview(Base):
    __tablename__ = 'courier_review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    client: Mapped['UserProfile'] = relationship('UserProfile', back_populates='reviews_courier',
                                                 foreign_keys=[client_id])
    courier_id: Mapped[int] = mapped_column(ForeignKey('courier.id'))
    courier: Mapped['Courier'] = relationship('Courier', back_populates='courier_reviews', foreign_keys=[courier_id])
    star: Mapped[StarChoices] = mapped_column(Enum(StarChoices))
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
