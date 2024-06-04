"""
`extra` field 설정을 통해 다양한 방법으로 모델을 생성할 수 있다.
- 관련 공식문서: https://docs.pydantic.dev/latest/api/config/
- 설정을 위해서는 Config 클래스를 설정하거나, ConfigDict를 사용한다.
  - model_config: ConfigDict 객체가 아닌 단순한 dict 객체이다.
- 관련 설정
  - extra: "ignore": 기본 설정 값으로, 모델에 없는 필드를 무시한다.
  - extra: "forbid": 모델에 없는 필드가 있을 경우, 에러(ValidationError)를 발생시킨다.
     - REST API에서 유용하다.(요청 데이터에 불필요한 필드가 있을 경우, 에러를 발생시킬 수 있기 때문)
  - extra: "allow": 모델에 없는 필드를 허용(필드 값이 모델에 추가 됨)한다. 단 아무런 검증이 이루어지지 않는다.
    - 전체 JSON Schema를  Pydantic 모델로 정의하는 대신 Pydantic 모델에서 필요한 부분(확인해야하는 부분)만 정의하고
     extra="allow"로 설정하여 관심있는 부분은 검증하고, 나머지 데이터는 그대로 사용할 수 있다.(=유효성 검사의 부담을 줄일 수 있다.)

설정된 추가 설정 값을 확인하기 위한 방법으로는 다음과 같은 방법이 있다.
- .model_extra: 설정된 extra 설정 값을 확인할 수 있다.
"""
from pydantic import BaseModel, ConfigDict


class NotHandlingExtraFields(BaseModel):
    field1: int


e1 = NotHandlingExtraFields(field1=1, field2=2)
print("e1: ", e1)  # 출력: e1:  ExtraFieldsHandling field1=1
print(dict(e1))  # 출력: {'field1': 1} | field2는 모델에 없는 필드이므로 나타나지 않는다.

print()
print("--------------------")


class DefaultExtraFields(BaseModel):
    field1: int
    model_config = ConfigDict(extra="ignore")


d1 = DefaultExtraFields(field1=1, field2=2)
print("d1: ", d1)  # 출력: d1:  DefaultExtraFields field1=1

print()


class ForbidExtraFields(BaseModel):
    field1: int
    model_config = ConfigDict(extra="forbid")


try:
    f1 = ForbidExtraFields(field1=1, field2=2)
except ValueError as ex:
    print(ex)
    """
    1 validation error for ForbidExtraFields
    field2
      Extra inputs are not permitted [type=extra_forbidden, input_value=2, input_type=int]
        For further information visit https://errors.pydantic.dev/2.7/v/extra_forbidden
    """

print()


class AllowExtraFields(BaseModel):
    field1: int
    model_config = ConfigDict(extra="allow")


a1 = AllowExtraFields(field1=1, field2=2)
print("a1: ", a1)  # 출력: a1:  AllowExtraFields field1=1
print(dict(a1))  # 출력: {'field1': 1, 'field2': 2} | field2는 모델에 없는 필드이지만, 허용되었기 때문에 나타난다.
print(a1.model_fields)  # 출력: {'field1': ModelField(name='field1', type=int, required=True)} | field2는 모델에 없는 필드이므로 나타나지 않는다.
print(a1.model_dump()) # 출력: {'field1': 1, 'field2': 2} | field2는 모델에 없는 필드이지만, 허용되었기 때문에 나타난다.