class ChoiceList:
    def __init__(self, values):
        if not isinstance(values, list):
            raise ValueError("선택지는 리스트여야 합니다.")
        if len(values) != 4:
            raise ValueError("선택지는 정확히 4개여야 합니다.")

        normalized_values = []
        for value in values:
            if not isinstance(value, str):
                raise ValueError("선택지는 문자열이어야 합니다.")

            normalized = value.strip()
            if not normalized:
                raise ValueError("선택지는 비어있을 수 없습니다.")
            normalized_values.append(normalized)

        self._values = tuple(normalized_values)

    @property
    def values(self):
        return list(self._values)
