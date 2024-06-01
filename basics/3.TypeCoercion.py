"""
Pydantic deserialize(역직렬화) 를 진행할 때, 유효성 검사(데이터 타입이 올바른지 확인하는 작업)이 존재한다.
- 모델 인스턴스 데이터가 올바른 유형으로 끝나는지 확인한다.
- 역직렬화를 위해 제공된 데이터의 유형이 일치하지 않는 경우, 데이터를 올바른 유형으로 "변환"하려고 시도한다.
  - 항상 유형을 강제하는 것은 아니다. (허용 가능한 유형 수준을 선택할 수 있다.) 설정에 따라 잘못된 데이터 유형이 제공될 때, 엄격하게 설정할 수 있다.
  - 유형 강제를 `lax`라고 이야기 하며, 다양한 유형 강제를 진행할 수 있다. 상황이 항상 "명확"한 것은 아니기 때문에 유형을 강제할 때 공식문서를 참고하여 작성하는 것이 좋다.
  - 관련 공식문서: https://docs.pydantic.dev/latest/concepts/conversion_table/

"""