from fastapi import APIRouter
from odmantic import AIOEngine

from core.task import (
    build_get_task_query,
    delete_task_by_obj,
    get_all_task_response,
    get_task_by_name,
)
from models.task import TaskModel
from schemas.task import (
    DeleteTaskResponse,
    MultipleTaskResponse,
    NewTask,
    SingleTaskResponse,
    UpdateTask,
)
from settings import EngineD

router = APIRouter()


@router.get("/task", response_model=MultipleTaskResponse)
async def get_tasks(engine: AIOEngine = EngineD):
    query = await build_get_task_query(engine)
    response = await get_all_task_response(engine, query)
    return response


@router.get("/task/{name}", response_model=SingleTaskResponse)
async def get_single_task(name: str, engine: AIOEngine = EngineD):
    task = await get_task_by_name(engine, name)
    return SingleTaskResponse(**task.dict())


@router.post("/task", response_model=SingleTaskResponse)
async def register_user(task: NewTask, engine: AIOEngine = EngineD):
    instance = TaskModel(**task.dict())
    await engine.save(instance)
    return SingleTaskResponse(**task.dict())


@router.put("/task/{name}", response_model=SingleTaskResponse)
async def update_task(
    name: str,
    update_data: UpdateTask,
    engine: AIOEngine = EngineD,
):
    task = await get_task_by_name(engine, name)
    for name, value in update_data.dict().items():
        setattr(task, name, value)
    await engine.save(task)
    return SingleTaskResponse(**task.dict())


@router.delete("/task/{name}")
async def delete_task(
    name: str,
    engine: AIOEngine = EngineD,
):
    task = await get_task_by_name(engine, name)
    if task:
        await delete_task_by_obj(engine, name)
    return DeleteTaskResponse(detail="Task deleted")
