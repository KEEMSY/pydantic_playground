"""
기본적으로 Pydantic에서는 숫자를 문자열로 강제로 변환할 수 없다. 하지만 설정을 통해 숫자 입력을 문자열로 변환할 수 있다.
- model_config = ConfigDict(coerce_numbers_to_str=True)
- model_config 설정 뿐만아니라, 사용자 지정 Validation을 지정하여 숫자를 문자열로 변환할 수 있다.
"""
from pydantic import BaseModel, ConfigDict


class StringNumberModel(BaseModel):
    field: str


try:
    s1 = StringNumberModel(field=1)
except ValueError as ex:
    print(ex)
    """
    1 validation error for StringNumberModel
    field
      str type expected (type=type_error.str)
    """
print()


class CoerceNumberToStringModel(BaseModel):
    field: str
    model_config = ConfigDict(coerce_numbers_to_str=True)


c = CoerceNumberToStringModel(field=1)
print(c)  # 출력: field='1'
