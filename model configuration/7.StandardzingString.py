"""
문자열을 관리하는 것은 HTTP 통신 및 API 통신에서 중요한 요소 중 하나이다.
- 공백(여백)을 제거하는 것은 문자열을 관리하는 중요한 요소 중 하나이다.

Pydantic에서는 문자열을 관리하는 방법을 제공한다.
- 공백 제거
- 문자열을 소문자로 변환
- 문자열을 대문자로 변환

"""

s1 = "  Hello, World!  "
s2 = "Hello, World!"
print(s1 == s2)  # 출력: False

from pydantic import BaseModel, ConfigDict


class Model(BaseModel):
    field: str

    model_config = ConfigDict(
        str_strip_whitespace=True
    )


m1 = Model(field="  Hello, World!  ")
m2 = Model(field="Hello, World!")

print(m1.dict())  # 출력: {'field': 'Hello, World!'}
print(m2.dict())  # 출력: {'field': 'Hello, World!'}

print(m1 == m2)  # 출력: True


class LowerCaseModel(BaseModel):
    field: str

    model_config = ConfigDict(str_to_lower=True)


m = LowerCaseModel(field="Hello, World!")
print(m.dict())  # 출력: {'field': 'hello, world!'}


class UpperCaseModel(BaseModel):
    field: str

    model_config = ConfigDict(str_to_upper=True)


m = UpperCaseModel(field="Hello, World!")
print(m.dict())  # 출력: {'field': 'HELLO, WORLD!'}
