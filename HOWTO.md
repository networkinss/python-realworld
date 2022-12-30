# How to add an API endpoint

## Add a line to api.py

```
Example
app.include_router(task_router, tags=["task"])
```

## Add task file in endpoints

Example:

```
from fastapi import APIRouter, Body
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


```

## Add task file to schemas

Example:

```
from typing import List

from pydantic import Field, constr

from .base import BaseSchema


class Task(BaseSchema):
    name: str = Field(..., example="generatesomething", title="name")
    enabled: str = Field(..., example="true", title="enabled")
    shell: str = Field(..., example="shellscript.sh", title="shell")
    firstarg: str = Field(..., example="any", title="firstarg")
    precheckfile: str = Field(..., example="/bin/binaryfile", title="precheckfile")
    args: List[str] = Field(..., example=["<appname>"], title="args")
    postcheckfile: List[str] = Field(
        ..., example=["openapi.yaml"], title="postcheckfile"
    )
    inputmustache: constr(min_length=3) = Field(
        ..., example="anyfilepath.mustache", title="inputmustache"
    )
    replacemustache: str = Field(..., example=".go", title="replacemustache")


class MultipleTaskResponse(BaseSchema):
    task: List[Task]


class SingleTaskResponse(Task):
    pass


class NewTask(Task):
    pass


class UpdateTask(Task):
    pass


class DeleteTaskResponse(BaseSchema):
    detail: str


```

## Add task file to core

Example:

```
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


```

# add task file in model

Example:

```
from typing import List

from odmantic import Model


class TaskModel(Model):
    name: str
    enabled: str
    shell: str
    firstarg: str
    precheckfile: str
    args: List[str]
    postcheckfile: List[str]
    inputmustache: str
    replacemustache: str

```

# add new exeption class for task in core/exceptions.py file

Example:

```
class TaskNotFoundException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

```

# How to add a lib with poetry

poetry add python-multipart
