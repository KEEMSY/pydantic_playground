"""
Pydantic 에서는 JSON Schema를 생성하는 메서드를 제공한다.
- 메서드: model_json_schema()
- 어떠한 이유로 JSON Schema를 수동으로 생성해야 하는 경우(요청된 Schema를 반환하는 API 엔드포인트가 있는 경우)유용하다.
"""
from pprint import pprint

from pydantic import BaseModel


class ForJSONModel(BaseModel):
    field_1: int | None = None
    field_2: str = "Python"


pprint(ForJSONModel.model_json_schema())
