from delivery_app.db.models import (UserProfile, Category, RefreshToken, Store, Contact, Product,
                                    Combo, Order, Courier, StoreReview, CourierReview)
from sqladmin import ModelView


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.id, UserProfile.username, UserProfile.first_name]
    name = 'Пользователь'
    name_plural = 'Пользователи'


class RefreshTokenAdmin(ModelView, model=RefreshToken):
    column_list = [UserProfile.id, RefreshToken.token, RefreshToken.user_id]


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.category_name]
    name = 'Категория'
    name_plural = 'Категории'


class StoreAdmin(ModelView, model=Store):
    column_list = [Store.id, Store.store_name, Store.category_id, Store.description,
                   Store.store_image, Store.address, Store.owner_id, Store.store_contact]


class ContactAdmin(ModelView, model=Contact):
    column_list = [Contact.id, Contact.title, Contact.contact_number, Contact.social_network, Contact.store_id]


class ProductAdmin(ModelView, model=Product):
    column_list = [Product.id, Product.product_name, Product.description, Product.product_image, Product.price,
                   Product.store_id]


class ComboAdmin(ModelView, model=Combo):
    column_list = [Combo.id, Combo.combo_name, Combo.description, Combo.price, Combo.store_id]


class OrderAdmin(ModelView, model=Order):
    column_list = [Order.id, Order.client_id]


class CourierAdmin(ModelView, model=Courier):
    column_list = [Courier.id, Courier.courier_id, Courier.order_id, Courier.courier_status]


class StoreReviewAdmin(ModelView, model=StoreReview):
    column_list = [StoreReview.id, StoreReview.client_id, StoreReview.store_id, StoreReview.text, StoreReview.star,
                   StoreReview.created_date]


class CourierReviewAdmin(ModelView, model=CourierReview):
    column_list = [CourierReview.id, CourierReview.client_id, CourierReview.courier_id, CourierReview.star,
                   CourierReview.created_date]
