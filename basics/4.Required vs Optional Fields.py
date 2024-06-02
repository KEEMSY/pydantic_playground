"""
Pydantic의 BaseModel을 사용하여 직렬화를 진행할 때, 필수 필드와 선택 필드에 대해 선택할 수 있다.
- Python에서는 인수의 기본값을 설정하여 선택적 필드를 만들 수 있다.
- Pydantic에서는 필드에 default 값을 설정하여 선택적 필드를 만들 수 있다.

필드의 기본 값을 지정할 때에는 매우 주의해야한다.
- Pydantic 의 기본 동작에서는 기본 값에 대한 유효성 검사를 진행하지 않는다.
- 이 부분은 개발자가 올바른 기본값을 제공하여 극복해야한다.(책임은 개발자에게 있다.)

* 참고사항: Pydantic 은 해당 값을 모델 인스턴스에 넣기 전에 해강 값의 유효성 검사를 진행한다.

추가적으로 함수 인수에 대한 기본값을 정의했을 때, 해당 값들은 함수 자체와 함께 계산 되고 저장 된다.
- 함수가 호출될 때마다 다시 생성 되지 않는다.(기본값은 모든 함수 호출 간에 공유된다.)

이와 관련하여 Pydantic은 기본 팩토리를 제공한다.
- Pydantic은 새로운 모델 인스턴스가 생성될 때마다 실제로 변경 가능한 깊은 복사본을 생성한다.

"""

from pydantic import BaseModel


class Circle(BaseModel):
    center: tuple[int, int] = (0, 0)
    radius: int


print("Circle.model_fields: ", Circle.model_fields)
# 출력: {'center': ModelField(name='center', type=Tuple[int, int], required=False, default=(0, 0)), 'radius': ModelField(name='radius', type=int, required=True)}
print()
print("--------------------")

c1 = Circle(radius=1)
print("c1: ", c1)
print()
print("--------------------")

data = {"radius": 1}
data_json = '{"radius": 1}'
c2 = Circle(**data)
c3 = Circle.model_validate(data)
print()
print("--------------------")

p4 = Circle(center=(1, 1), radius=2)

print()
print("--------------------")


class ModelWithDefaultValue(BaseModel):
    field: int = "Python"


m1 = ModelWithDefaultValue()
print(m1)
print()
print("--------------------")

print("Python의 예시")
from time import time


def extend_list(user_list: list = []):
    user_list.append(int(time()))
    return user_list


my_times = []
extend_list(my_times)
print("my_times: ", my_times)
print()

my_times = extend_list()
print("my_times: ", my_times)

my_new_times = extend_list()  # 문제가 되는 부분: 함수의 기본 값은 모든 함수 호출 간에 공유 된다.
print("my_new_times: ", my_new_times)

print()
print("--------------------")
