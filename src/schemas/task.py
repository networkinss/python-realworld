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
    inputmustache: List[str] = Field(
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
