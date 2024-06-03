"""
Nullable 필드와 Optional 필드는 차이가 있다.
- Optional 필드는 단순히 deserialized 되는 데이터에 해당 특정 필드의 값이 포함될 필요가 없음을 의미 하며, 이 경우 미리 정의된 기본 값이 사용 된다.
- Nullable 필드는 선택 사항 여부와 무관 하다. 기본적으로 필드를 없음(또는 JSON의 null)관점으로 설정할 수 있는지 여부를 나타낸다.

Nullable 필드 임을 Pydantic 으로 표현하기 위해서는 타입힌트를 사용해야 한다.
- Type | None Python (3.10 이상)
- Union[Type, None]
- default_value=None 을 할 때에는 Nullable 이 가능함을 표기해야 한다. -> default: int|None =None

Nullable 필드와 Optional 필드가 함께 사용되는 경우가 많다.
- 단순히 데이터에값이 제공되지 않았음을 나타내기 위해 기본 값을 없음으로 설정하는 경우가 많다.

Python 3.10 이전 버전의 Python에서는 OptionaL을 사용하지 않는 것이 좋다.
- 필드가 Optional 임을 나타내는 것이 아닌 nullable 임을 나타내기 때문이다.

요약 한다면, field 는 다음의 상태를 가질 수 있으며, 각 조합을 검증 측면에서 의미를 알아둘 필요가 있다.
- 가능한 상태
  - nullable and not nullable
  - required and optional
- 가능한 조합
  - required and not nullable
  - required and nullable
  - optional and not nullable
  - optional and nullable
"""
from typing import Optional, Union

from pydantic import BaseModel, ValidationError


class NotNullableAndNotOptionalModel(BaseModel):
    field: int


try:
    NotNullableAndNotOptionalModel(field=None)
except ValidationError as ex:
    print(ex)

print()

try:
    NotNullableAndNotOptionalModel()
except ValidationError as ex:
    print(ex)

print()
print("--------------------")


class NullableAndNotOptionalModel(BaseModel):
    field: int | None


n1 = NullableAndNotOptionalModel(field=1)
n2 = NullableAndNotOptionalModel(field=None)

try:
    n3 = NullableAndNotOptionalModel()  # Nullable 하다는 것이, Optional 하다는 것은 아니다.
except ValidationError as ex:
    print(ex)

print()
print("--------------------")


class Model(BaseModel):
    field: int | None = None  # Python 3.10 이상 가능, 이하 버전에서는 Union[int, None] 사용


print()
print("--------------------")


class OptionalTypingModel(BaseModel):
    # Python 3.10 이전 버전의 Python에서는 OptionaL을 사용하지 않는 것이 좋다.
    # 필드가 Optional 임을 나타내는 것이 아닌 nullable 임을 나타내기 때문이다.
    field: Optional[int]


try:
    Model()
except ValidationError as ex:
    print(ex)
    """
    1 validation error for Model
    field
      Field required [type=missing, input_value={}, input_type=dict]
    """


class ModifiedOptionalTypingModel(BaseModel):
    field: Optional[int] = None


m1 = ModifiedOptionalTypingModel()
print("m1: ", m1)
print("ModifiedOptionalTypingModel.model_fields: ", ModifiedOptionalTypingModel.model_fields)

print()
print("--------------------")


class Model(BaseModel):
    field_1: int | None
    field_2: Union[int, None]
    field_3: Optional[int]


print("Model.model_fields: ", Model.model_fields)
print()
print("--------------------")


class RequiredAndNotNullableModel(BaseModel):
    """
    field를 정의하는 방법의 기본이 되는 방법
    - field required 이고, 오직 int 형만 가능하다.(Not Nullable)
    """
    field: int


print()

try:
    RequiredAndNotNullableModel()
except ValidationError as ex:
    print(ex)
    """
    1 validation error for RequiredAndNotNullableModel
    field
      Field required [type=missing, input_value={}, input_type=dict]
    """

print()

try:
    RequiredAndNotNullableModel(field=None)
except ValidationError as ex:
    print(ex)
    """
    1 validation error for RequiredAndNotNullableModel
    field
      none is not an allowed value [type=type_error.none.not_allowed]
    """

print()
print("--------------------")


class RequiredAndNullableModel(BaseModel):
    """
    필드를 필수로 만들기 위해 기본값을 지정하지 않고, 타입 힌팅을 사용하여 None이 가능함을 표현한다.
    """
    field: int | None


try:
    RequiredAndNullableModel()
except ValidationError as ex:
    print(ex)
    """
    1 validation error for RequiredAndNullableModel
    field
      Field required [type=missing, input_value={}, input_type=dict]
    """

print()

print((RequiredAndNullableModel(field=None)))  # 출력: RequiredAndNullableModel field=None

print()
print("--------------------")


class OptionalAndNotNullableModel(BaseModel):
    """
    필드가 선택적이지만, None이 아닌 값으로 설정해야 함에 주의한다.(Not Nullable임에도 기본 값을 None으로 설정해도 에러가 발생하지 않는다.)

    """
    field: int = 0


print(OptionalAndNotNullableModel())  # 출력: OptionalAndNotNullableModel field=0

try:
    OptionalAndNotNullableModel(field=None)
except ValidationError as ex:
    print(ex)
    """
    1 validation error for OptionalAndNotNullableModel
    field
      none is not an allowed value [type=type_error.none.not_allowed]
    """

print()
print("--------------------")


class OptionalAndNullableModel(BaseModel):
    """
    Nullable 필드에 가장 흔히 사용되는 방법이며, None을 default로 지정하여, Optional 필드로 만든다.
    """
    field: int | None = None


print(OptionalAndNullableModel())  # 출력: OptionalAndNullableModel field=None
print(OptionalAndNullableModel(field=None))  # 출력: OptionalAndNullableModel field=None
