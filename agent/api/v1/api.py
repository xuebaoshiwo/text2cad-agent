from fastapi import APIRouter

api_router = APIRouter()

# 在这里导入和包含其他路由
# from .endpoints import items, users
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(items.router, prefix="/items", tags=["items"]) 