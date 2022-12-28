# How to add an API endpoint

## Add a line to api.py

Mustache
app.include_router({{task}}\_router, tags=["{{task}}"])
Example
app.include_router(task_router, tags=["task"])

## Add file in endpoints

Example:

```
from fastapi import APIRouter
from odmantic import AIOEngine

from core.tag import get_all_tags
from schemas.tag import TagsResponse
from settings import EngineD

router = APIRouter()


@router.get("/tags", response_model=TagsResponse)
async def get_tags(engine: AIOEngine = EngineD):
    tags = await get_all_tags(engine)
    return TagsResponse(tags=tags)

```

## Add file to schemas

Example:

```
from typing import List

from .base import BaseSchema


class TagsResponse(BaseSchema):
    tags: List[str]

```

## Ad file to core

Example:

```
from typing import List

from odmantic import AIOEngine

from models.article import ArticleModel


async def get_all_tags(engine: AIOEngine) -> List[str]:
    pipeline = [
        {
            "$unwind": {
                "path": ++ArticleModel.tag_list,
                "preserveNullAndEmptyArrays": True,
            }
        },
        {
            "$group": {
                "_id": "all",
                "all_tags": {"$addToSet": ++ArticleModel.tag_list},
            }
        },
    ]
    col = engine.get_collection(ArticleModel)
    result = await col.aggregate(pipeline).to_list(length=1)
    if len(result) > 0:
        tags: List[str] = result[0]["all_tags"]
    else:
        tags = []
    return tags

```

# How to add a lib with poetry

poetry add python-multipart
