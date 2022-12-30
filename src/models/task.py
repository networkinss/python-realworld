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
