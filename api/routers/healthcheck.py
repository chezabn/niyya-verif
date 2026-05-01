from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.dependencies import CommonDependencies

router = APIRouter(tags=["Healthcheck"])


class SystemInfo(BaseModel):
    environment: str
    description: str
    version: str


class HealthCheck(BaseModel):
    title: str
    status: str
    system_info: SystemInfo


@router.get("/healthcheck", response_model=HealthCheck)
async def healthcheck(deps: CommonDependencies = Depends()):
    return {
        "title": deps.cfg.title,
        "status": "OK",
        "system_info": {
            "environment": deps.cfg.environment,
            "description": deps.cfg.description,
            "version": deps.cfg.version,
        },
    }
