"""
pydantic을 사용하여 모델을 정의하다보면, 모델 설정 코드가 중복 되는 경우가 많다.(단순 반복되는 동일한 조건의 코드들)
이를 해결하기 위한 방법으로 Python 에서 제공하는 anooteated types 를 사용하여 해당 문제를 해결할 수 있다.
- Pythond 에서는 모든 타입에 메타 데이터를 첨부하는 메커니즘이 존재한다. 이를 Annotated Types라고 한다.
- Pydantic에서 Annotated를 사용하면, Field를 통해 제약이 포함된 재사용 가능한 타입을 정의할 수 있다.
  - 여러 모델에서 동일한 제약 조건을 반복적으로 작성하지 않을 수 있다.
- Annotated Types는 Python 3.9부터 지원한다.
  - Annotated[타입, 메타데이터1, 메타데이터2, ...]
  - get_args(): Annotated에 전달된 인수들을 반환한다. 이를 통해 메타데이터가 어떻게 구성되어 있는지 쉽게 확인할 수 있다.

주의해야 할 사항
- Annotated는 메타데이터를 제공하지만, 직접적으로 검증이나 동작을 수행하지 않는다.
- 메타데이터를 해석하고 적용하는 것은 사용하는 라이브러리(Pydantic 등)의 역할이다.
- Pydantic은 이러한 메타데이터를 사용하여 필드의 제약 조건을 설정하고, 데이터의 유효성을 검사할 수 있다.

"""
from typing import Annotated, get_args

from pydantic import BaseModel, Field, ValidationError

SpecialInt = Annotated[int, "metadata 1", [1, 2, 3], 100]  # 메타 데이터를 추가한다.
print(get_args(SpecialInt))  # 출력: (<class 'int'>, 'metadata 1', [1, 2, 3], 100),


class Model(BaseModel):
    x: int = Field(gt=0, le=100)
    y: int = Field(gt=0, le=100)
    z: int = Field(gt=0, le=100)


print(Model.model_fields)
# 출력:
# {'x': FieldInfo(annotation=int, required=True, metadata=[Gt(gt=0), Le(le=100)]),
# 'y': FieldInfo(annotation=int, required=True, metadata=[Gt(gt=0), Le(le=100)]),
# 'z': FieldInfo(annotation=int, required=True, metadata=[Gt(gt=0), Le(le=100)])}

BoundedInt = Annotated[int, Field(gt=0, le=100)]


class Model(BaseModel):
    x: BoundedInt
    y: BoundedInt
    z: BoundedInt


print(Model.model_fields)
# 출력:
# {'x': FieldInfo(annotation=int, required=True, metadata=[Gt(gt=0), Le(le=100)]),
# 'y': FieldInfo(annotation=int, required=True, metadata=[Gt(gt=0), Le(le=100)]),
# 'z': FieldInfo(annotation=int, required=True, metadata=[Gt(gt=0), Le(le=100)])}

"""
유형을 동적으로 선언하는 방법
- Any를 사용하는 방법: Pydantic을 사용하는 의미가 사라지게 된다.
- Python에서 제공하는 TypeVar를 사용하는 방법: TypeVar를 사용하여 동적으로 유형을 선언할 수 있다.

T = TypeVar('T')를 사용하여 동적으로 유형을 선언할 수 있다.
"""

from typing import TypeVar

T = TypeVar('T')
BoundedList = Annotated[list[T], Field(max_length=10)]

print(BoundedList[
          int])  # 출력: typing.Annotated[list[int], FieldInfo(annotation=NoneType, required=True, metadata=[MaxLen(max_length=10)])]
print(BoundedList[
          str])  # 출력: typing.Annotated[list[str], FieldInfo(annotation=NoneType, required=True, metadata=[MaxLen(max_length=10)])]


class Model(BaseModel):
    integers: BoundedList[int] = []
    strings: BoundedList[str] = []


print(Model())  # 출력: integers=[], strings=[]

try:
    Model(integers=[0.5])
except ValidationError as ex:
    print(ex)

    """
    1 validation error for Model
    integers.0
      Input should be a valid integer, got a number with a fractional part [type=int_from_float, input_value=0.5, input_type=float]
        For further information visit https://errors.pydantic.dev/2.7/v/int_from_float
    """

"""
[ 핃드 레벨에서 문자열 조작하기 ]

문자열 제약조건을 Field 를 조작함으로써 할 수 있으나, 해당 방법 이외에 모델 수준에서 사용할수 있는 StringConstraints 가 존재한다.
- StringConstraints: Pydantic에서 제공하는 문자열 제약 조건을 정의하는 클래스
- 최소길이(혹은 최대 길이), 정규식 패턴만 필요한 경우 Feild를 사용하고, 그 외의 경우 StringConstraints를 사용한다.
- 공식 문서: https://docs.pydantic.dev/latest/api/types/#pydantic.types.AllowInfNan


| 속성           | 자료형                  | 설명                                           |
|--------------------|----------------------------|----------------------------------------------------|
| `strip_whitespace` | `bool` \| `None`            | 앞뒤 공백을 제거할지 여부                          |
| `to_upper`         | `bool` \| `None`            | 문자열을 대문자로 변환할지 여부                    |
| `to_lower`         | `bool` \| `None`            | 문자열을 소문자로 변환할지 여부                    |
| `strict`           | `bool` \| `None`            | 문자열을 엄격한 모드에서 검증할지 여부             |
| `min_length`       | `int` \| `None`             | 문자열의 최소 길이                                 |
| `max_length`       | `int` \| `None`             | 문자열의 최대 길이                                 |
| `pattern`          | `str` \| `Pattern[str]` \| `None` | 문자열이 일치해야 하는 정규 표현식 패턴              |

"""

from typing import Annotated
from pydantic import StringConstraints

StandardString = Annotated[
    str,
    StringConstraints(to_lower=True, min_length=2, strip_whitespace=True)
]


class Model(BaseModel):
    code: StandardString | None = None


print(Model(code="ABC   ")) # 출력: code='abc'

try:
    Model(code="   a   ")
except ValidationError as ex:
    print(ex)
    """
    1 validation error for Model
    code
      String should have at least 2 characters [type=string_too_short, input_value='   a   ', input_type=str]
        For further information visit https://errors.pydantic.dev/2.7/v/string_too_short
    """