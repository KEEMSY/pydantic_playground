"""
Pydantic은 기본값의 유효성 검사를 하지 않는다. 기본 값을 검증하지 않는다면, 필드를 잘못 정의하게 될 수 있음을 의미한다.
- Pydantic 모델을 만들어 우리가 원하는 기본 값을 설정할 수 있지만, 이러한 기본값이 유효한가에 대한 책임은 개발자에게 있다.
- 기본 값을 검증하는 것은, 데이터 또는 데이터를 기반으로 하는 다른 필드의 모집단이 일부 변환하는 경우 유용하며, 병렬화되는 데이터에서 값이 나오든 기본값에서 나오든 동일한 유효성을 유지할 수 있다.

다행히도(?) Pydantic에서는 Model Level, 혹은 Field Level에서 기본값을 검증하도록 할 수 있다.
- Model Level: model_config = ConfigDict(validate_default=True)를 사용한다.
- Field Level: field(..., validate_default=True)를 사용한다.
"""
from pydantic import BaseModel, ConfigDict, Field


class WrongModel(BaseModel):
    field_1: int = None
    field_2: str = 100


w1 = WrongModel()  # 잘못된 값이 선언되었지만, 에러가 발생하지 않음
print(w1)
print()

try:
    WrongModel(field_1=None, field_2=100)
except ValueError as ex:
    print(ex)
    """
    2 validation errors for WrongModel
    field_1
      Input should be a valid integer [type=int_type, input_value=None, input_type=NoneType]
        For further information visit https://errors.pydantic.dev/2.7/v/int_type
    field_2
      Input should be a valid string [type=string_type, input_value=100, input_type=int]
        For further information visit https://errors.pydantic.dev/2.7/v/string_type
    """

print()
print("--------------------")


class ModelLevelValidateDefault(BaseModel):
    model_config = ConfigDict(validate_default=True)

    field_1: int = None
    field_2: str = 100


try:
    ModelLevelValidateDefault()
except ValueError as ex:
    print(ex)
    """
    2 validation errors for ModelLevelValidateDefault
    field_1
      Input should be a valid integer [type=int_type, input_value=None, input_type=NoneType]
        For further information visit https://errors.pydantic.dev/2.7/v/int_type
    field_2
      Input should be a valid string [type=string_type, input_value=100, input_type=int]
        For further information visit https://errors.pydantic.dev/2.7/v/string_type
    """

print()
print("--------------------")


class FieldLevelValidateDefault(BaseModel):
    field_1: int = Field(default=None, validate_default=True)
    field_2: str = Field(default=100, validate_default=True)


try:
    FieldLevelValidateDefault()
except ValueError as ex:
    print(ex)
    """
    2 validation errors for FieldLevelValidateDefault
    field_1
      Input should be a valid integer [type=int_type, input_value=None, input_type=NoneType]
        For further information visit https://errors.pydantic.dev/2.7/v/int_type
    field_2
      Input should be a valid string [type=string_type, input_value=100, input_type=int]
        For further information visit https://errors.pydantic.dev/2.7/v/string_type
    """