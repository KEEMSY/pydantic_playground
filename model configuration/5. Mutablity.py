"""
기본적으로 Pydantic 모델은 수정가능하다. 즉, 모델 인스턴스가 생성된 뒤, 인스턴스의 값을 수정할 수 있다.
그러나 설정을 통해 모델 인스턴스의 값을 수정할 수 없도록 할 수 있다.
- model_config = ConfigDict(frozen=True)
- 모델을 Immutable로 설정한다는 것은, 모델 인스턴스를 dictionary의 key 값으로 사용할 수 있다는 사이드이펙트가 존재한다.
"""
from pydantic import BaseModel, ConfigDict


class MutableModel(BaseModel):
    a: int
    b: int


m = MutableModel(a=1, b=2)
m.a = 10
print(m.dict())  # 출력: {'a': 10, 'b': 2}
print()

try:
    d = {m: "model"}
except TypeError as ex:
    print(ex)
    """
    unhashable type: 'MutableModel'
    """

print()
print("--------------------")


class ImmutableModel(BaseModel):
    a: int
    b: int
    model_config = ConfigDict(frozen=True)


m1 = ImmutableModel(a=1, b=2)
try:
    m1.a = 10
except ValueError as ex:
    print(ex)
    """
    1 validation error for ImmutableModel
a
  Instance is frozen [type=frozen_instance, input_value=10, input_type=int]
    For further information visit https://errors.pydantic.dev/2.7/v/frozen_instance

    """

print()

d = {m1: "model"}
print(d)  # 출력: {ImmutableModel(a=1, b=2): 'model'}