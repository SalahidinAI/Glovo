from fastapi import FastAPI
from sqladmin import Admin
from .views import UserProfileAdmin, CategoryAdmin, RefreshTokenAdmin, StoreAdmin, ContactAdmin, ProductAdmin, \
    ComboAdmin, OrderAdmin, CourierAdmin, StoreReviewAdmin, CourierReviewAdmin
from delivery_app.db.database import engine


def setup_admin(app: FastAPI):
    admin = Admin(app, engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(RefreshTokenAdmin)
    admin.add_view(StoreAdmin)
    admin.add_view(ContactAdmin)
    admin.add_view(ProductAdmin)
    admin.add_view(ComboAdmin)
    admin.add_view(OrderAdmin)
    admin.add_view(CourierAdmin)
    admin.add_view(StoreReviewAdmin)
    admin.add_view(CourierReviewAdmin)
