"""
느슨한 유형 변환은 Pydantic이 입력을 유효한 유형으로 변환할 수 있는 경우 수행된다.
- Tuple -> List
- List -> Tuple
- Int -> Float

하지만 이러한 유형 변환은 원하는 행동이 아닐 수 있다. 그리고 이와 관련하여, 느슨하게(또는 엄격하게) 유형 변환을 사용할 수 있다.
- 혹은 필드 단위로 유형 변환을 사용할 수 있다.
- model_config = ConfigDict(strict=True)를 사용하여 엄격한 유형 변환을 사용할 수 있다.
- 관련 공식문서: https://docs.pydantic.dev/latest/concepts/conversion_table/

JSON 데이터를 역직렬화 할 때는 동작이 다름에 주의해아한다.
- boolean: true or false(소문자 주의)
- number(float 또는 int는 실제로 중요하지 않음)
- string: "string" (따옴표 주의, 큰 따옴표를 사용해야 한다.)
- null: 문자열 null으로 표시되며, 따옴표를 붙이지 않는다.
- array(배열): 대괄호, Array 또는 객체를 포함한 임의의 JSON 유형의 쉼표로 구분된 값
- object(객체): 기본적으로 접힌 괄호(`{`)으로 구분된 dictionary. key는 문자열이어야 하며, value는 객체 자체를 포함한 모든 JSON 유형이 가능하다.
"""

from pydantic import BaseModel, ValidationError, ConfigDict


class LooseExampleModel(BaseModel):
    field_1: str
    field_2: float
    field_3: list
    field_4: tuple


try:
    LooseExampleModel(field_1=100, field_2=1, field_3=(1, 2, 3), field_4=[1, 2, 3])
except ValidationError as ex:
    print(ex)
    """
    1 validation error for ExampleModel
    field_1
      Input should be a valid string [type=string_type, input_value=100, input_type=int]
        For further information visit https://errors.pydantic.dev/2.7/v/string_type
    """

print()
print("--------------------")


class StrictExampleModel(BaseModel):
    model_config = ConfigDict(strict=True)

    field_1: str
    field_2: float
    field_3: list
    field_4: tuple


try:
    StrictExampleModel(field_1=100, field_2=1, field_3=(1, 2, 3), field_4=[1, 2, 3])
except ValidationError as ex:
    print(ex)
    """
    3 validation errors for StrictExampleModel
    field_1
      Input should be a valid string [type=string_type, input_value=100, input_type=int]
        For further information visit https://errors.pydantic.dev/2.7/v/string_type
    field_3
      Input should be a valid list [type=list_type, input_value=(1, 2, 3), input_type=tuple]
        For further information visit https://errors.pydantic.dev/2.7/v/list_type
    field_4
      Input should be a valid tuple [type=tuple_type, input_value=[1, 2, 3], input_type=list]
        For further information visit https://errors.pydantic.dev/2.7/v/tuple_type
    """