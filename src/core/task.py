from typing import Optional

from odmantic import AIOEngine
from odmantic.query import QueryExpression, desc

from core.exceptions import TaskNotFoundException
from models.task import TaskModel
from schemas.task import MultipleTaskResponse


async def build_get_task_query(
    engine: AIOEngine,
) -> Optional[QueryExpression]:
    # query = QueryExpression()
    # query &= TaskModel
    query = ()
    return query


async def get_all_task_response(
    engine: AIOEngine,
    query: QueryExpression,
) -> MultipleTaskResponse:
    tasks = await engine.find(
        TaskModel,
        query,
        sort=desc(TaskModel.id),
    )
    return MultipleTaskResponse(task=tasks)


async def get_task_by_name(engine: AIOEngine, name: str) -> TaskModel:
    task = await engine.find_one(TaskModel, TaskModel.name == name)
    if task is None:
        raise TaskNotFoundException()
    return task


async def delete_task_by_obj(engine: AIOEngine, name: str):
    res = await engine.find_one(TaskModel, TaskModel.name == name)
    await engine.delete(res)
    return True
