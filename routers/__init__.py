from routers.category import app as category_router
from routers.products import app as products_router
from routers.users import app as users_router
from routers.user_profile import app as users_profile_router

from fastapi import APIRouter

app_router = APIRouter()
app_router.include_router(category_router)
app_router.include_router(products_router)
app_router.include_router(users_router)
app_router.include_router(users_profile_router)
