"""
Pydantic은 역직렬화(Deserialization) 시에 데이터 검증(validation)을 수행 한다.
그러나 모델 인스턴스의 데이터를 수정할 때, 기본적으로 유효성 검사를 진행하지 않는다.
모델 인스턴스의 데이터를 수정할 때, 유효성 검사를 진행하기 위해서는 model_config 설정을 해야 한다.
- model_config = ConfigDict(validate_assignment=True)
"""

from pydantic import BaseModel, ConfigDict


class Model(BaseModel):
    a: int
    b: int


m = Model(a=1, b=2)
m.a = "a"
print(m.dict())  # 출력: {'a': 'a', 'b': 2} | a는 int로 정의되어 있지만, str로 변경되었다.
print()
print("--------------------")


class ModelWithValidateAssignment(BaseModel):
    a: int
    b: int
    model_config = ConfigDict(validate_assignment=True)


m1 = ModelWithValidateAssignment(a=1, b=2)

try:
    m1.a = "a"
except ValueError as ex:
    print(ex)
    """
    1 validation error for ModelWithValidateAssignment
    a
      Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='a', input_type=str]
        For further information visit https://errors.pydantic.dev/2.7/v/int_parsing

    """
