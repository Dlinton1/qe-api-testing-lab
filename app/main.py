import os
from typing import Annotated, Optional

from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="QE Property API", version="1.0.0")

API_TOKEN = os.getenv("QE_API_TOKEN", "local-test-token")
properties: list[dict] = []
next_property_id = 1


class PropertyCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    monthly_rent: float = Field(gt=0, le=1_000_000)


class PropertyResponse(BaseModel):
    id: int
    name: str
    monthly_rent: float


def require_auth(
    authorization: Annotated[Optional[str], Header()] = None,
) -> None:
    expected = f"Bearer {API_TOKEN}"
    if authorization != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing bearer token",
        )


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get(
    "/api/properties",
    response_model=list[PropertyResponse],
    dependencies=[Depends(require_auth)],
)
def list_properties() -> list[dict]:
    return properties


@app.post(
    "/api/properties",
    response_model=PropertyResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_auth)],
)
def create_property(payload: PropertyCreate) -> dict:
    global next_property_id

    record = {
        "id": next_property_id,
        "name": payload.name,
        "monthly_rent": payload.monthly_rent,
    }
    properties.append(record)
    next_property_id += 1
    return record
