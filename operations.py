# operations.py

from fastapi import APIRouter, HTTPException, Path
from typing import List

from repository.database import SessionLocal, DBOperationRecord, DBOperationRecordSchema

import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/operations", tags=["operations"])

print("✅ operations.py LOADED")  # Indicates the file has been loaded

# ---------- GET All Operations ----------
@router.get("", response_model=List[DBOperationRecordSchema])
async def get_all_operations():
    print("✅ /v1/operations/ HIT")
    db = SessionLocal()
    try:
        records = db.query(DBOperationRecord).all()
        print("✅ Returning:", records)
        return [DBOperationRecordSchema.model_validate(r) for r in records]
    finally:
        db.close()


# ---------- GET Operation by ID ----------
@router.get("/{operation_id}", response_model=DBOperationRecordSchema)
async def get_operation(operation_id: int = Path(..., gt=0)):
    db = SessionLocal()
    try:
        record = db.query(DBOperationRecord).filter(DBOperationRecord.id == operation_id).first()
        if record is None:
            raise HTTPException(status_code=404, detail="Operation not found")
        return DBOperationRecordSchema.model_validate(record)
    finally:
        db.close()


# ---------- DELETE Operation by ID ----------
@router.delete("/{operation_id}")
async def delete_operation(operation_id: int = Path(..., gt=0)):
    db = SessionLocal()
    try:
        record = db.query(DBOperationRecord).filter(DBOperationRecord.id == operation_id).first()
        if not record:
            raise HTTPException(status_code=404, detail="Operation not found")
        db.delete(record)
        db.commit()
        return {"detail": f"Operation with ID {operation_id} deleted successfully"}
    finally:
        db.close()


# ---------- DELETE All Operations ----------
@router.delete("/")
async def delete_all_operations():
    db = SessionLocal()
    try:
        deleted = db.query(DBOperationRecord).delete()
        db.commit()
        return {"detail": f"{deleted} operations deleted successfully"}
    finally:
        db.close()
