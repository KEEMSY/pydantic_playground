from pydantic import BaseModel, ValidationError

"""
Pydantic 클래스는 일반적인 Python 클래스라고 말할 수 있다.
- BaseModel 클래스를 상속하여, 속성과 메서드를 추가한 개념으로 이해하면 쉽다.
- 각각의 필드에는 required=True가 기본 값으로 설정 되어 있어서 필수 필드로 간주 된다.
  - 필드 값을 선언하지 않을 경우, 에러(ValidationError)가 발생한다.
  - 일반적으로 API 호출자에게 JSON Payload에 문제가 있을 경우 매우 디버깅에 유용 하다.(== REST API에 유용하다.)
- 기본 BaseModel을 사용할 경우(Config 설정이 없을 경우), 모델을 생성한 이후, 값을 새롭게 할당할 때 Validate가 진행되지 않는다.
"""


class Person(BaseModel):
    first_name: str
    last_name: str
    age: int


# 예시
p = Person(first_name='Seongyeon', last_name='Kim', age=29)
print(repr(p))  # 출력: Person(first_name='John', last_name='Doe', age=30)
print(p.model_fields) # 출력: {'first_name': ModelField(name='first_name', type=str, required=True), 'last_name': ModelField(name='last_name', type=str, required=True), 'age': ModelField(name='age', type=int, required=True)}
print(p.first_name)  # 출력: Seongyeon

# ValidationError: 데이터 형식이 올바르지 않을 경우, 에러가 발생한다.
try:
    Person(last_name='Wrong Seongyeon', age=29)
except ValidationError as ex:
    print(ex)
    """
    출력:
    1 validation error for Person
    first_name
      Field required [type=missing, input_value={'last_name': 'Error Seongyeon', 'age': 29}, input_type=dict]
        For further information visit https://errors.pydantic.dev/2.7/v/missing
    """


# 모델 생성 방법(2가지)
# 1. dict를 사용하여 모델 생성하기

# 1.1. 언패킹 연산자(**)를 사용하여 모델 생성
dict_data = {
    'first_name': 'Seongyeon',
    'last_name': 'Kim',
    'age': 29
}
deserializing_by_dict_p_1 = Person(**dict_data)
print(repr(deserializing_by_dict_p_1))  # 출력: Person(first_name='Seongyeon', last_name='Kim', age=29)

# 1.2. model_validate() 메서드를 사용하여 모델 생성
deserializing_by_dict_p_2 = Person.model_validate(dict_data)
print(repr(deserializing_by_dict_p_2))  # 출력: Person(first_name='Seongyeon', last_name='Kim', age=29)

# 2. JSON 문자열을 사용하여 모델 생성하기

# JSON 데이터 예시
json_data = '''
{
    "first_name": "Seongyeon",
    "last_name": "Kim",
    "age": 29
}
'''

# model_validate_json() 메서드를 사용하여 모델 생성
deserializing_by_json_p_1 = Person.model_validate_json(json_data)
print(repr(deserializing_by_json_p_1))  # 출력: Person(first_name='Seongyeon', last_name='Kim', age=29)


# ValidationError: JSON 데이터 형식이 올바르지 않을 경우, 에러가 발생한다.
missing_data_json = '''
{
    "last_name": "Wrong Kim"
}
'''

try:
    Person.model_validate_json(missing_data_json)
except ValidationError as ex:
    print(ex)
    """
    2 validation errors for Person
    first_name
      Field required [type=missing, input_value={'last_name': 'Newton'}, input_type=dict]
        For further information visit https://errors.pydantic.dev/2.7/v/missing
    age
      Field required [type=missing, input_value={'last_name': 'Newton'}, input_type=dict]
        For further information visit https://errors.pydantic.dev/2.7/v/missing
    """