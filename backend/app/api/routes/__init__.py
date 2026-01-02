"""API routes package initialization."""

from app.api.routes.chat import router as chat_router
from app.api.routes.faqs import router as faq_router
from app.api.routes.documents import router as document_router
from app.api.routes.admin import router as admin_router
from app.api.routes.telegram import router as telegram_router

__all__ = [
    "chat_router",
    "faq_router",
    "document_router",
    "admin_router",
    "telegram_router",
]
