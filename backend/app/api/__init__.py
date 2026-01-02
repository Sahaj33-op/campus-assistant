"""API package initialization."""

from app.api.routes import (
    chat_router,
    faq_router,
    document_router,
    admin_router,
    telegram_router,
)

__all__ = [
    "chat_router",
    "faq_router",
    "document_router",
    "admin_router",
    "telegram_router",
]
