"""
Pydantic deserialize(역직렬화) 를 진행할 때, 유효성 검사(데이터 타입이 올바른지 확인하는 작업)이 존재한다.
- 모델 인스턴스 데이터가 올바른 유형으로 끝나는지 확인한다.
- 역직렬화를 위해 제공된 데이터의 유형이 일치하지 않는 경우, 데이터를 올바른 유형으로 "변환"하려고 시도한다.
  - 항상 유형을 강제하는 것은 아니다. (허용 가능한 유형 수준을 선택할 수 있다.) 설정에 따라 잘못된 데이터 유형이 제공될 때, 엄격하게 설정할 수 있다.
  - 유형 강제를 `lax`라고 이야기 하며, 다양한 유형 강제를 진행할 수 있다. 상황이 항상 "명확"한 것은 아니기 때문에 유형을 강제할 때 공식문서를 참고하여 작성하는 것이 좋다.
  - 관련 공식문서: https://docs.pydantic.dev/latest/concepts/conversion_table/

"""
from pydantic import BaseModel, ValidationError


class Coordinate(BaseModel):
    x: float
    y: float


c1 = Coordinate(x=1.1, y=-2.2)
print(c1)  # 출력: x=1.1 y=-2.2
print("Coordinate.model_fields: ",
      Coordinate.model_fields)  # 출력: {'x': ModelField(name='x', type=float, required=True), 'y': ModelField(name='y', type=float, required=True)}
print("type(c1.x): ", type(c1.x))  # 출력: <class 'float'>
print()
print("--------------------")

c0 = Coordinate(x=0, y='-2.2')
print("type(c0.x): ", type(c0.x))  # 출력: <class 'float'>
print("type(c0.y): ", type(c0.y))  # 출력: <class 'float'>
print()
print("--------------------")


class Contact(BaseModel):
    email: str


initial_json_data = '''
{
    "email": "inewton@principia.com"
}
'''
print("Contact.model_validate_json(initial_json_data): ", Contact.model_validate_json(initial_json_data))
print()
print("--------------------")

new_json_data = '''
{
    "email": {
        "personal": "inewton@principia.com",
        "work": "isaac.newton@themint.com"
    }
}
'''
try:
    Contact.model_validate_json(new_json_data)
except ValidationError as ex:
    print(ex)

print()
print("--------------------")

new_data = {
    "email": {
        "personal": "inewton@principia.com",
        "work": "isaac.newton@themint.com"
    }
}
print("Contact(email=str(new_data['email']): ", Contact(email=str(new_data['email'])))
