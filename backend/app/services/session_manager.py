"""
Session Management Service.
Handles conversation context and session persistence.
"""

import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from loguru import logger

from app.models.database import Session, Message, User, MessageRole


class SessionManager:
    """
    Manages conversation sessions and context.
    Maintains conversation history for multi-turn interactions.
    """

    # Session timeout in hours
    SESSION_TIMEOUT = 24

    # Maximum messages to keep in context
    MAX_CONTEXT_MESSAGES = 10

    async def create_session(
        self,
        db: AsyncSession,
        platform: str = "web",
        user_id: Optional[str] = None,
        language: str = "en",
    ) -> Session:
        """Create a new conversation session."""
        session_id = str(uuid.uuid4())

        # Find or create user
        db_user = None
        if user_id:
            result = await db.execute(
                select(User).where(User.external_id == user_id)
            )
            db_user = result.scalar_one_or_none()

            if not db_user:
                db_user = User(
                    external_id=user_id,
                    platform=platform,
                    preferred_language=language,
                )
                db.add(db_user)
                await db.flush()

        # Create session
        session = Session(
            session_id=session_id,
            user_id=db_user.id if db_user else None,
            platform=platform,
            language=language,
            context={},
            is_active=True,
        )
        db.add(session)
        await db.commit()
        await db.refresh(session)

        logger.info(f"Created new session: {session_id}")
        return session

    async def get_session(
        self,
        db: AsyncSession,
        session_id: str,
    ) -> Optional[Session]:
        """Get session by ID."""
        result = await db.execute(
            select(Session)
            .options(selectinload(Session.messages))
            .where(Session.session_id == session_id)
        )
        session = result.scalar_one_or_none()

        if session:
            # Check if session is expired
            if self._is_session_expired(session):
                await self._close_session(db, session)
                return None

            # Update last activity
            session.updated_at = datetime.utcnow()
            await db.commit()

        return session

    async def get_or_create_session(
        self,
        db: AsyncSession,
        session_id: Optional[str],
        platform: str = "web",
        user_id: Optional[str] = None,
        language: str = "en",
    ) -> Session:
        """Get existing session or create new one."""
        if session_id:
            session = await self.get_session(db, session_id)
            if session:
                return session

        return await self.create_session(db, platform, user_id, language)

    async def add_message(
        self,
        db: AsyncSession,
        session: Session,
        role: MessageRole,
        content: str,
        original_content: Optional[str] = None,
        original_language: Optional[str] = None,
        intent: Optional[str] = None,
        confidence: Optional[int] = None,
        sources: Optional[List[Dict]] = None,
    ) -> Message:
        """Add a message to the session."""
        message = Message(
            session_id=session.id,
            role=role,
            content=content,
            original_content=original_content,
            original_language=original_language,
            intent=intent,
            confidence=confidence,
            sources=sources,
        )
        db.add(message)
        await db.commit()
        await db.refresh(message)

        logger.debug(f"Added {role.value} message to session {session.session_id}")
        return message

    async def get_conversation_history(
        self,
        db: AsyncSession,
        session: Session,
        limit: int = None,
    ) -> List[Dict[str, str]]:
        """Get conversation history for context."""
        limit = limit or self.MAX_CONTEXT_MESSAGES

        result = await db.execute(
            select(Message)
            .where(Message.session_id == session.id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        messages = result.scalars().all()

        # Reverse to get chronological order
        history = []
        for msg in reversed(messages):
            history.append({
                "role": msg.role.value,
                "content": msg.content,
            })

        return history

    async def update_session_context(
        self,
        db: AsyncSession,
        session: Session,
        context_updates: Dict[str, Any],
    ):
        """Update session context."""
        current_context = session.context or {}
        current_context.update(context_updates)
        session.context = current_context
        await db.commit()

    async def update_session_language(
        self,
        db: AsyncSession,
        session: Session,
        language: str,
    ):
        """Update session language preference."""
        session.language = language
        await db.commit()

    async def close_session(
        self,
        db: AsyncSession,
        session_id: str,
    ) -> bool:
        """Close a session."""
        result = await db.execute(
            select(Session).where(Session.session_id == session_id)
        )
        session = result.scalar_one_or_none()

        if session:
            await self._close_session(db, session)
            return True
        return False

    async def _close_session(self, db: AsyncSession, session: Session):
        """Mark session as inactive."""
        session.is_active = False
        await db.commit()
        logger.info(f"Closed session: {session.session_id}")

    def _is_session_expired(self, session: Session) -> bool:
        """Check if session has expired."""
        if not session.updated_at:
            return False

        expiry_time = session.updated_at + timedelta(hours=self.SESSION_TIMEOUT)
        return datetime.utcnow() > expiry_time

    async def cleanup_expired_sessions(self, db: AsyncSession) -> int:
        """Clean up expired sessions. Run periodically."""
        expiry_threshold = datetime.utcnow() - timedelta(hours=self.SESSION_TIMEOUT)

        result = await db.execute(
            update(Session)
            .where(
                Session.is_active == True,
                Session.updated_at < expiry_threshold,
            )
            .values(is_active=False)
        )
        await db.commit()

        count = result.rowcount
        if count > 0:
            logger.info(f"Cleaned up {count} expired sessions")
        return count

    async def get_active_sessions_count(self, db: AsyncSession) -> int:
        """Get count of active sessions."""
        result = await db.execute(
            select(Session).where(Session.is_active == True)
        )
        return len(result.scalars().all())


# Singleton instance
_session_manager: Optional[SessionManager] = None


def get_session_manager() -> SessionManager:
    """Get or create session manager instance."""
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager
