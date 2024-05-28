from pydantic import BaseModel


class Person(BaseModel):
    first_name: str
    last_name: str
    age: int


# 가장 일반적인 방법으로 모델 생성
p = Person(first_name='John', last_name='Doe', age=30)
print(repr(p))  # 출력: Person(first_name='John', last_name='Doe', age=30)

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
