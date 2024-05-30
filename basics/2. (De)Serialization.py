"""
# Serialization(직렬화): 객체들의 데이터를 전송할 수 있도록 특정 포맷 상태로 변환하는 것
# Deserialization(역직렬화): 직렬화된 데이터를 다시 객체 형태로 만드는 것

`1.Pydantic의 BaseModel 사용하기.py` 에서 작성한 BaseModel을 사용하는 것은 Deserialization(역직렬화)이다.
- dict를 사용하여 모델 생성하기
- JSON 문자열을 사용하여 모델 생성하기

2. 에서는 Serialization(직렬화)의 방밥에 대해 정리한다.
- Python 객체를 dict로 변환하기
- BaseModel 에서 제공하는 메서드를 사용하는 방

Pydantic에서 제공하는 BaseModel 클래스 내에는 다양한 직렬화 메서드를 제공한다.
- model_dump(): BaseModel을 `dict`로 변환한다.
- model_dump_json(): BaseModel을 `JSON 문자열`로 변환한다.


model_dump_json()의 경우 다양한 설정 값이 존재하여, 유용하게 사용할 수 있다.
- indent: JSON 출력의 들여스기 수준을 지정한다. None(값을 설정하지 않음) 경우, 출력은 축약형(압축된 형태)으로 생성된다.
- exclude: JOSN 출력에서 제외할 필드를 지정한다. 리스트 혹은 딕셔너리 형태로 지정할 수 있다.
- context: 시리얼라이저로 전달할 추가 컨텍스트를 지정한다. 사용자 정의 직렬화 로직에 사용하면 유용하다.
- by_alias: True로 설정 시, 필드 이름 대신 별칭(alias)을 사용하여 JSON을 직렬화 한다.
- exclude_unset: True로 설정 시, 명시적으로 설정되지 않은 필드를 JSON 출력에서 제외한다.
- exclude_default: True로 설정 시, 기본값으로 설정된 필드를 JSON 출력에서 제외한다.
- exclude_none: True로 설정 시, 값이 None인 필드를 JSON 출력에서 제외한다.
- round_trip: True로 설정 시, 덤프된 값이 Json[T]와 같은 비멱등(non-indempotent) 타입의 입력으로 보장한다.
- warnigs: 직렬화 오류를 처리하는 방식을 지정한다.
  - False, none: 오류를 무시한다.
  - True, warn: 오류를 로그로 기록한다.
  - error: PaydanticSerializationError를 발생시킨다.
- serialize_as_any: True 설정 시, 필드의 덕 타이핑 직렬화 동작을 활성화 한다.
"""


from pydantic import BaseModel


class Person(BaseModel):
    first_name: str
    last_name: str
    age: int


data = {'first_name': 'Seongyeon', 'last_name': 'Kim', 'age': 29}
json_data = '{"first_name": "Seongyeon", "last_name": "Kim", "age": 29}'
# deserialize 방법 1
p1 = Person(first_name='Seongyeon', last_name='Kim', age=29)
# deserialize 방법 2
p2 = Person(**data)
# deserialize 방법 3
p3 = Person.model_validate(data)
# deserialize 방법 4
p4 = Person.model_validate_json(json_data)

# serialize 방법 1
print(p1.__dict__)  # 출력: {'first_name': 'Seongyeon', 'last_name': 'Kim', 'age': 29}
# serialize 방법 2
print(p1.model_dump())  # 출력: {'first_name': 'Seongyeon', 'last_name': 'Kim', 'age': 29}
print(type(p1.model_dump()))  # 출력: <class 'dict'>
# serialize 방법 3
print(p1.model_dump_json())  # 출력: {"first_name": "Seongyeon", "last_name": "Kim", "age": 29}
print(p1.model_dump_json())  # 출력: <class 'str'>
print(p1.model_dump_json(indent=2))  # escape characters 를 보기좋게 사용할 수 있다.
print(p1.model_dump_json(
    exclude={'age'}))  # 출력: {"first_name": "Seongyeon", "last_name": "Kim"} exclude 옵션을 사용하여 특정 필드를 제외할 수 있다.
