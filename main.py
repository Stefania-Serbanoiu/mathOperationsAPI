# main.py

from fastapi import FastAPI
from models import OperationRequest, OperationResult
from controller import compute_operation

app = FastAPI()


@app.post("/compute", response_model=OperationResult)
async def compute(request: OperationRequest):
    return compute_operation(request)