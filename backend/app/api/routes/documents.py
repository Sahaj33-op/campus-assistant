"""
Document Management API Routes.
Endpoints for uploading and managing documents (PDFs, DOCX, etc.).
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from loguru import logger

from app.core.database import get_db
from app.models.database import Document
from app.models.schemas import DocumentUploadResponse, DocumentInfo
from app.services.document_processor import get_document_processor
from app.services.vector_store import get_vector_store

router = APIRouter(prefix="/documents", tags=["Documents"])

# Allowed file types
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc", ".txt"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@router.get("/", response_model=List[DocumentInfo])
async def list_documents(
    category: Optional[str] = None,
    indexed_only: bool = False,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    """
    List all uploaded documents.
    """
    query = select(Document)

    if category:
        query = query.where(Document.category == category)
    if indexed_only:
        query = query.where(Document.is_indexed == True)

    query = query.order_by(Document.uploaded_at.desc())
    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    documents = result.scalars().all()

    return documents


@router.get("/{doc_id}", response_model=DocumentInfo)
async def get_document(doc_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get document information by ID.
    """
    result = await db.execute(select(Document).where(Document.id == doc_id))
    doc = result.scalar_one_or_none()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    return doc


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    category: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    auto_index: bool = Form(True),
    db: AsyncSession = Depends(get_db),
):
    """
    Upload a document for processing and indexing.

    Supported formats: PDF, DOCX, DOC, TXT
    Max file size: 10 MB
    """
    # Validate file extension
    filename = file.filename or "unknown"
    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Supported: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    # Read file content
    content = await file.read()

    # Validate file size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE // (1024*1024)} MB",
        )

    try:
        processor = get_document_processor()

        # Save file
        file_path, unique_filename = await processor.save_uploaded_file(
            content, filename
        )

        # Create database entry
        doc = Document(
            filename=unique_filename,
            original_filename=filename,
            file_type=ext,
            file_path=file_path,
            category=category,
            description=description,
            is_indexed=False,
            chunk_count=0,
        )
        db.add(doc)
        await db.commit()
        await db.refresh(doc)

        # Index document if requested
        chunk_count = 0
        if auto_index:
            chunk_count = await _index_document(doc, processor)
            doc.is_indexed = True
            doc.chunk_count = chunk_count
            await db.commit()

        logger.info(f"Uploaded document: {filename} -> {unique_filename}")

        return DocumentUploadResponse(
            id=doc.id,
            filename=unique_filename,
            file_type=ext,
            is_indexed=doc.is_indexed,
            chunk_count=chunk_count,
            message=f"Document uploaded successfully. {chunk_count} chunks indexed.",
        )

    except Exception as e:
        await db.rollback()
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(status_code=500, detail="Error uploading document")


@router.post("/{doc_id}/index")
async def index_document(doc_id: int, db: AsyncSession = Depends(get_db)):
    """
    Index a document that was uploaded without auto-indexing.
    """
    result = await db.execute(select(Document).where(Document.id == doc_id))
    doc = result.scalar_one_or_none()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    if doc.is_indexed:
        return {"message": "Document already indexed", "chunk_count": doc.chunk_count}

    try:
        processor = get_document_processor()
        chunk_count = await _index_document(doc, processor)

        doc.is_indexed = True
        doc.chunk_count = chunk_count
        await db.commit()

        logger.info(f"Indexed document: {doc.id} with {chunk_count} chunks")

        return {
            "message": "Document indexed successfully",
            "chunk_count": chunk_count,
        }

    except Exception as e:
        logger.error(f"Error indexing document: {e}")
        raise HTTPException(status_code=500, detail="Error indexing document")


@router.delete("/{doc_id}")
async def delete_document(doc_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a document and remove from vector store.
    """
    result = await db.execute(select(Document).where(Document.id == doc_id))
    doc = result.scalar_one_or_none()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    try:
        # Remove from vector store
        vector_store = get_vector_store()
        await vector_store.delete_by_source(doc.filename)

        # Delete file
        processor = get_document_processor()
        processor.delete_file(doc.file_path)

        # Delete from database
        await db.delete(doc)
        await db.commit()

        logger.info(f"Deleted document: {doc_id}")
        return {"message": "Document deleted successfully"}

    except Exception as e:
        await db.rollback()
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail="Error deleting document")


@router.get("/stats/summary")
async def get_document_stats(db: AsyncSession = Depends(get_db)):
    """
    Get document statistics.
    """
    result = await db.execute(select(Document))
    documents = result.scalars().all()

    total_docs = len(documents)
    indexed_docs = sum(1 for d in documents if d.is_indexed)
    total_chunks = sum(d.chunk_count for d in documents)

    # Count by file type
    by_type = {}
    for doc in documents:
        by_type[doc.file_type] = by_type.get(doc.file_type, 0) + 1

    # Count by category
    by_category = {}
    for doc in documents:
        cat = doc.category or "uncategorized"
        by_category[cat] = by_category.get(cat, 0) + 1

    return {
        "total_documents": total_docs,
        "indexed_documents": indexed_docs,
        "total_chunks": total_chunks,
        "by_file_type": by_type,
        "by_category": by_category,
    }


async def _index_document(doc: Document, processor) -> int:
    """Helper to index document in vector store."""
    vector_store = get_vector_store()

    # Process document into chunks
    chunks = await processor.process_file(
        doc.file_path,
        metadata={
            "document_id": doc.id,
            "category": doc.category,
            "original_filename": doc.original_filename,
        },
    )

    # Add to vector store
    await vector_store.add_documents(chunks)

    return len(chunks)
