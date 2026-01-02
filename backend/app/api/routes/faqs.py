"""
FAQ Management API Routes.
Admin endpoints for managing FAQ entries.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from loguru import logger

from app.core.database import get_db
from app.models.database import FAQ
from app.models.schemas import FAQCreate, FAQUpdate, FAQResponse
from app.services.document_processor import get_document_processor
from app.services.vector_store import get_vector_store

router = APIRouter(prefix="/faqs", tags=["FAQs"])


@router.get("/", response_model=List[FAQResponse])
async def list_faqs(
    category: Optional[str] = None,
    language: Optional[str] = None,
    active_only: bool = True,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    """
    List all FAQs with optional filtering.
    """
    query = select(FAQ)

    if category:
        query = query.where(FAQ.category == category)
    if language:
        query = query.where(FAQ.language == language)
    if active_only:
        query = query.where(FAQ.is_active == True)

    query = query.order_by(FAQ.priority.desc(), FAQ.created_at.desc())
    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    faqs = result.scalars().all()

    return faqs


@router.get("/categories")
async def list_categories(db: AsyncSession = Depends(get_db)):
    """
    Get list of all FAQ categories.
    """
    result = await db.execute(
        select(FAQ.category).distinct().where(FAQ.category.isnot(None))
    )
    categories = [row[0] for row in result.fetchall()]

    return {"categories": categories}


@router.get("/{faq_id}", response_model=FAQResponse)
async def get_faq(faq_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a specific FAQ by ID.
    """
    result = await db.execute(select(FAQ).where(FAQ.id == faq_id))
    faq = result.scalar_one_or_none()

    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")

    return faq


@router.post("/", response_model=FAQResponse)
async def create_faq(
    faq_data: FAQCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new FAQ entry.
    """
    try:
        # Create FAQ in database
        faq = FAQ(
            question=faq_data.question,
            answer=faq_data.answer,
            category=faq_data.category,
            language=faq_data.language,
            keywords=faq_data.keywords,
            priority=faq_data.priority,
        )
        db.add(faq)
        await db.commit()
        await db.refresh(faq)

        # Index in vector store
        await _index_faq(faq)

        logger.info(f"Created FAQ: {faq.id}")
        return faq

    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating FAQ: {e}")
        raise HTTPException(status_code=500, detail="Error creating FAQ")


@router.put("/{faq_id}", response_model=FAQResponse)
async def update_faq(
    faq_id: int,
    faq_data: FAQUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Update an existing FAQ.
    """
    result = await db.execute(select(FAQ).where(FAQ.id == faq_id))
    faq = result.scalar_one_or_none()

    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")

    try:
        # Update fields
        update_data = faq_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(faq, field, value)

        await db.commit()
        await db.refresh(faq)

        # Re-index in vector store
        vector_store = get_vector_store()
        await vector_store.delete_faq(faq_id)
        if faq.is_active:
            await _index_faq(faq)

        logger.info(f"Updated FAQ: {faq_id}")
        return faq

    except Exception as e:
        await db.rollback()
        logger.error(f"Error updating FAQ: {e}")
        raise HTTPException(status_code=500, detail="Error updating FAQ")


@router.delete("/{faq_id}")
async def delete_faq(faq_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete an FAQ entry.
    """
    result = await db.execute(select(FAQ).where(FAQ.id == faq_id))
    faq = result.scalar_one_or_none()

    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")

    try:
        # Remove from vector store
        vector_store = get_vector_store()
        await vector_store.delete_faq(faq_id)

        # Delete from database
        await db.delete(faq)
        await db.commit()

        logger.info(f"Deleted FAQ: {faq_id}")
        return {"message": "FAQ deleted successfully"}

    except Exception as e:
        await db.rollback()
        logger.error(f"Error deleting FAQ: {e}")
        raise HTTPException(status_code=500, detail="Error deleting FAQ")


@router.post("/bulk-import")
async def bulk_import_faqs(
    faqs: List[FAQCreate],
    db: AsyncSession = Depends(get_db),
):
    """
    Bulk import multiple FAQs.
    """
    created_count = 0
    errors = []

    for i, faq_data in enumerate(faqs):
        try:
            faq = FAQ(
                question=faq_data.question,
                answer=faq_data.answer,
                category=faq_data.category,
                language=faq_data.language,
                keywords=faq_data.keywords,
                priority=faq_data.priority,
            )
            db.add(faq)
            await db.flush()
            await _index_faq(faq)
            created_count += 1

        except Exception as e:
            errors.append({"index": i, "error": str(e)})

    await db.commit()

    return {
        "created": created_count,
        "errors": errors,
        "total": len(faqs),
    }


@router.post("/reindex")
async def reindex_all_faqs(db: AsyncSession = Depends(get_db)):
    """
    Reindex all FAQs in vector store.
    """
    try:
        # Get all active FAQs
        result = await db.execute(
            select(FAQ).where(FAQ.is_active == True)
        )
        faqs = result.scalars().all()

        # Clear existing FAQ entries from vector store
        vector_store = get_vector_store()

        # Re-index each FAQ
        indexed_count = 0
        for faq in faqs:
            await _index_faq(faq)
            indexed_count += 1

        logger.info(f"Reindexed {indexed_count} FAQs")
        return {"indexed": indexed_count}

    except Exception as e:
        logger.error(f"Error reindexing FAQs: {e}")
        raise HTTPException(status_code=500, detail="Error reindexing FAQs")


async def _index_faq(faq: FAQ):
    """Helper to index FAQ in vector store."""
    processor = get_document_processor()
    vector_store = get_vector_store()

    chunks = await processor.process_faq(
        question=faq.question,
        answer=faq.answer,
        category=faq.category,
        faq_id=faq.id,
    )
    await vector_store.add_documents(chunks)
