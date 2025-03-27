from fastapi import FastAPI, Depends, HTTPException
from delivery_app.db.database import SessionLocal
from delivery_app.db.schema import ContactSchema, ProductSchema, ComboSchema, OrderSchema, \
    CourierSchema, \
    StoreReviewSchema, CourierReviewSchema
from delivery_app.db.models import Contact, Product, Combo, Order, Courier, StoreReview, CourierReview
from sqlalchemy.orm import Session
import redis.asyncio as aioredis
from contextlib import asynccontextmanager
from fastapi_limiter import FastAPILimiter
from delivery_app.api.endpoints import category, courier, courier_review, contact, order, auth, store, store_review, product, combo
from delivery_app.admin.setup import setup_admin
import uvicorn
from starlette.middleware.sessions import SessionMiddleware
from delivery_app.config import SECRET_KEY


async def init_redis():
    return aioredis.from_url('redis://localhost', encoding='utf-8', decode_responses=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = await init_redis()
    await FastAPILimiter.init(redis)
    yield
    await redis.close()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

delivery_app = FastAPI(title='Delivery site', lifespan=lifespan)
delivery_app.add_middleware(SessionMiddleware, secret_key="SECRET_KEY")
setup_admin(delivery_app)

delivery_app.include_router(auth.auth_router)
delivery_app.include_router(category.category_router)
delivery_app.include_router(courier.courier_router)
delivery_app.include_router(courier_review.courier_review_router)
delivery_app.include_router(product.product_router)
delivery_app.include_router(store.store_router)
delivery_app.include_router(store_review.store_review_router)
delivery_app.include_router(contact.contact_router)
delivery_app.include_router(combo.combo_router)
delivery_app.include_router(order.order_router)

if __name__ == '__main__':
    uvicorn.run(delivery_app, host='127.0.0.1', port=8000)
