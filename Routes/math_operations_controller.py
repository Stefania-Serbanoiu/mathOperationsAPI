from fastapi import APIRouter, HTTPException, Path, Request
from typing import List
from fastapi import Depends
import logging
from Authorization.authorization_dependencies import verify_bearer_token
from Model.models import OperationResult, OperationRequest
from Repository.database import (SessionLocal, DBOperationRecord)
from Repository.database import DBOperationRecordSchema
from Routes.math_operations_async_mechanism import enqueue_math_operation


logger = logging.getLogger(__name__)


router = APIRouter(prefix="/v1/operations", tags=["operations"])


# POST : submit a math operation
@router.post("/compute", response_model=OperationResult)
async def compute(request: OperationRequest, _: Request):
    logger.info(f"Received compute request: {request.model_dump()}")
    return await enqueue_math_operation(request)


# GET All Operations
@router.get("", response_model=List[DBOperationRecordSchema])
async def get_all_operations(_: Request):
    logger.info("Fetching all operation records")
    db = SessionLocal()
    try:
        records = db.query(DBOperationRecord).all()
        logger.info(f"Retrieved {len(records)} records")
        return [DBOperationRecordSchema.model_validate(r) for r in records]
    finally:
        db.close()


# GET Operation by ID
@router.get("/{operation_id}", response_model=DBOperationRecordSchema)
async def get_operation(operation_id: int = Path(..., gt=0),
                        _: Request = None):
    logger.info(f"Fetching operation by ID: {operation_id}")
    db = SessionLocal()
    try:
        record = (db.query(DBOperationRecord).
                  filter(DBOperationRecord.id == operation_id).first())
        if record is None:
            logger.warning(f"Operation ID {operation_id} not found")
            raise HTTPException(status_code=404, detail="Operation not found")
        logger.info(f"Found record for ID {operation_id}")
        return DBOperationRecordSchema.model_validate(record)
    finally:
        db.close()


# DELETE Operation by ID
@router.delete("/{operation_id}")
async def delete_operation(operation_id: int = Path(..., gt=0),
                           _: Depends = Depends(verify_bearer_token),
                           __: Request = None):
    logger.info(f"Attempting to delete operation ID: {operation_id}")
    db = SessionLocal()
    try:
        record = (db.query(DBOperationRecord).
                  filter(DBOperationRecord.id == operation_id).first())
        if not record:
            logger.warning(f"Operation ID {operation_id} "
                           f"not found for deletion")
            raise HTTPException(status_code=404, detail="Operation not found")
        db.delete(record)
        db.commit()
        logger.info(f"Deleted operation ID: {operation_id}")
        return {"detail": f"Operation with ID "
                          f"{operation_id} deleted successfully"}
    finally:
        db.close()


# DELETE All Operations
@router.delete("/")
async def delete_all_operations(_: Depends = Depends(verify_bearer_token),
                                __: Request = None):
    logger.info("Deleting all operations")
    db = SessionLocal()
    try:
        deleted = db.query(DBOperationRecord).delete()
        db.commit()
        logger.info(f"Deleted {deleted} operations")
        return {"detail": f"{deleted} operations deleted successfully"}
    finally:
        db.close()
