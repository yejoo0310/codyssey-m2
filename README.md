# Quiz Game Architecture

이 문서는 이 프로젝트가 왜 `model`과 `vo`를 분리했는지, 그리고 레이어를 어떤 기준으로 나누었는지 설명하는 아키텍처 문서입니다.

이 프로젝트의 핵심 목표는 "기능이 동작한다"에서 끝나지 않고, 객체가 자기 책임을 가지도록 구조를 정리하는 것입니다.  
그래서 컨트롤러가 모든 규칙을 직접 처리하지 않고, 값은 `vo`로 감싸고, 도메인 규칙은 `model`이 담당하도록 설계했습니다.

## 전체 구조

```text
main
  -> controller
       -> view
       -> repository
            -> repository abs
            -> json file repository implementations
                 -> json files
       -> model
            -> vo
```

현재 디렉터리 책임은 다음과 같습니다.

- `main.py`
  - 프로그램 진입점입니다.
  - `QuizGame`과 `ConsoleView`를 조립합니다.
- `controller.py`
  - 전체 흐름을 제어합니다.
  - 메뉴 분기, 퀴즈 시작, 퀴즈 추가, 저장 호출 같은 유스케이스를 담당합니다.
- `view.py`
  - 사용자 입력과 출력을 담당합니다.
  - 입력 문자열을 파싱하고, 결과 메시지를 보여줍니다.
- `repository/`
  - 저장소 인터페이스와 구현체를 담당합니다.
  - 추상 저장소와 JSON 파일 구현체를 분리했습니다.
- `model/`
  - 퀴즈, 퀴즈 목록, 최고 기록처럼 도메인의 상태와 행위를 담당합니다.
- `vo/`
  - 문제, 선택지, 정답, 명령처럼 의미 있는 값을 표현합니다.
  - 값이 올바른지 검증하는 책임을 가집니다.

## 왜 `model`과 `vo`를 분리했는가

객체지향에서 중요한 것은 "데이터를 어디에 둘까"보다 "책임을 누가 가져야 하는가"입니다.

이 프로젝트는 원시값을 그대로 흘려보내지 않기 위해 `vo`를 사용합니다.

- `"파이썬"`은 그냥 문자열이 아니라 `Question`
- `"A"`는 그냥 문자열이 아니라 `Choice`
- `["A", "B", "C", "D"]`는 그냥 리스트가 아니라 `Choices`
- `2`는 그냥 숫자가 아니라 `Answer`
- `1`은 그냥 숫자가 아니라 `Command`

이렇게 하면 다음 장점이 생깁니다.

- 값이 생성되는 순간부터 유효성을 보장할 수 있습니다.
- 컨트롤러가 `"비어있나?"`, `"1~4 범위인가?"` 같은 규칙을 중복해서 검사하지 않아도 됩니다.
- 숫자 `2`가 "정답 번호 2"인지, "메뉴 번호 2"인지 문맥이 분명해집니다.

반대로 `model`은 이 값들을 조합해서 실제 도메인 행위를 수행합니다.

- `MultipleChoiceQuiz`
  - 질문, 선택지, 정답으로 하나의 퀴즈를 표현합니다.
- `Quizzes`
  - 퀴즈 목록을 다루는 일급 컬렉션입니다.
- `BestRecord`
  - 최고 점수 계산과 갱신 규칙을 직접 가집니다.

즉, `vo`는 "값이 올바른가"를 담당하고, `model`은 "그 값들로 무엇을 하는가"를 담당합니다.

## 레이어별 역할

### 1. Main

`main.py`는 객체를 조립만 합니다.

```python
from controller import QuizGame
from view import ConsoleView


def main() -> None:
    game = QuizGame(ConsoleView())
    game.run()
```

여기서 중요한 점은, `main`이 프로그램의 시작점이지만 비즈니스 규칙은 전혀 알지 못한다는 것입니다.
실제 저장소도 같은 방식으로 조립됩니다. 컨트롤러는 추상 저장소 타입으로 다루고, 실제 객체는 JSON 파일 구현체를 사용합니다.

### 2. Controller

`QuizGame`은 "무엇을 할지"를 결정합니다.

- 메뉴 선택에 따라 기능을 분기
- 저장소에서 상태 로드
- 뷰에서 받은 입력을 도메인 객체로 변환
- 도메인 객체의 결과를 바탕으로 다음 흐름 결정

하지만 `QuizGame`은 직접 출력 포맷을 만들지 않고, JSON을 직접 읽지도 않으며, 값 검증을 세부적으로 처리하지도 않습니다.

예를 들어 새 퀴즈를 만들 때도 컨트롤러는 원시 입력을 받아 VO로 승격시키는 경계 역할만 합니다.

```python
def create_quiz(
    self, question: str, choices: list[str], answer: int
) -> MultipleChoiceQuiz:
    choices_vo = Choices.from_texts(choices)
    return MultipleChoiceQuiz(
        Question(question),
        choices_vo,
        Answer(answer, choices_vo),
    )
```

이 메서드는 원시 입력을 직접 들고 도메인 안으로 들어가지 않도록 막아주는 경계입니다.

### 3. View

`ConsoleView`는 "어떻게 보여줄지"와 "어떻게 입력받을지"를 담당합니다.

- 메뉴 출력
- 입력 문자열 수집
- 숫자 파싱
- 결과 메시지 출력

중요한 점은 View가 도메인 규칙을 직접 소유하지 않는다는 것입니다.

예를 들어 정답 입력은:

1. View가 문자열을 받습니다.
2. View가 `int`로 파싱합니다.
3. `Answer` VO를 생성합니다.
4. `Answer`가 유효하지 않으면 VO가 만든 에러 메시지를 그대로 출력합니다.

즉, 파싱 실패는 View가 처리하지만, "이 값이 정답으로 유효한가?"는 `Answer`가 결정합니다.

### 4. Repository

Repository는 저장소의 역할과 저장 방식의 구현을 분리합니다.

- `QuizRepository`
  - 퀴즈 저장소의 추상 인터페이스입니다.
  - 컨트롤러는 이 타입에 의존합니다.
- `StateRepository`
  - 최고 기록 저장소의 추상 인터페이스입니다.
  - 컨트롤러는 이 타입에 의존합니다.
- `JsonFileQuizRepository`
  - `quiz.json`, `default-quiz.json`을 다루는 JSON 파일 구현체입니다.
- `JsonFileStateRepository`
  - `state.json`을 다루는 JSON 파일 구현체입니다.

이 구조의 핵심은 도메인 객체가 `to_dict()`, `from_dict()`를 몰라도 된다는 점입니다.  
직렬화는 도메인의 책임이 아니라 저장소 경계의 책임으로 내려갔습니다.

이렇게 인터페이스와 구현체를 나누면, 나중에 저장 방식이 바뀌어도 컨트롤러 전체를 고치지 않고 구현체만 교체할 수 있습니다.

### 5. Model

`model`은 도메인의 상태와 행위를 가집니다.

#### `MultipleChoiceQuiz`

- `Question`, `Choices`, `Answer`를 조합해서 하나의 퀴즈를 만듭니다.
- 정답 판정은 `is_correct()`로 수행합니다.
- 정답 출력용 표현은 `answer_label()`로 제공합니다.

```python
quiz = MultipleChoiceQuiz(
    Question("Python의 창시자는 누구인가?"),
    Choices.from_texts(["Guido", "James", "Dennis", "Bjarne"]),
    Answer(1, Choices.from_texts(["Guido", "James", "Dennis", "Bjarne"])),
)
```

실제 코드에서는 같은 `Choices` 객체를 재사용합니다. 핵심은 퀴즈가 원시 문자열과 숫자 묶음이 아니라, 의미를 가진 객체들의 조합이라는 점입니다.

#### `Quizzes`

`Quizzes`는 단순한 `list` 래퍼가 아니라 일급 컬렉션입니다.

- `add()`
- `count()`
- `is_empty()`
- `has_minimum()`
- `items()`

이렇게 목록을 컬렉션 객체로 감싸면, 컨트롤러가 직접 `append`, `len`, 빈 리스트 판별을 여기저기 하지 않아도 됩니다.

#### `BestRecord`

최고 기록 갱신 규칙은 `BestRecord`가 스스로 알고 있습니다.

```python
is_new_best = best_record.update(total_count, best_count)
```

이 호출 하나로:

- 점수 계산
- 최고 기록 비교
- 상태 갱신
- 갱신 여부 반환

이 모두 처리됩니다.  
이것이 "행동하는 객체"의 예시입니다.

### 6. VO

VO는 값 자체에 의미와 규칙을 부여합니다.

#### `Question`

- 문자열이어야 함
- 공백 제거 후 비어 있으면 안 됨

#### `Choice`

- 문자열이어야 함
- 공백 제거 후 비어 있으면 안 됨

#### `Choices`

- `Choice` 4개를 가져야 함
- 텍스트 목록이 필요하면 `texts()`로 변환

#### `Answer`

- 정수여야 함
- `Choices` 개수 범위 안에 있어야 함
- `label()`로 `"2번"` 같은 표현을 제공
- `matches()`로 다른 `Answer`와 비교

#### `Command`

- 메뉴 번호는 1~5만 허용
- `is_play_quiz()`, `is_add_quiz()` 같은 의미 있는 메시지를 제공

## 객체지향 원칙을 어떻게 적용했는가

### SRP: 단일 책임 원칙

한 객체가 한 가지 책임만 가지도록 분리했습니다.

- `ConsoleView`: 입력과 출력
- `QuizRepository`, `StateRepository`: 저장
- `Question`, `Answer`, `Command`: 값 검증
- `MultipleChoiceQuiz`, `BestRecord`: 도메인 행위
- `QuizGame`: 전체 흐름 제어

예전처럼 컨트롤러 하나가 입력, 출력, 검증, 저장, 점수 계산을 모두 갖고 있으면 수정 범위가 커집니다.  
지금 구조는 변경 이유별로 클래스를 나누었습니다.

### SOLID 관점의 분리

이 프로젝트는 완전한 프레임워크 수준의 SOLID를 모두 강하게 적용한 구조는 아니지만, 다음 원칙을 분명히 따르고 있습니다.

- `S`
  - 책임이 섞이지 않도록 레이어와 객체를 나눴습니다.
- `O`
  - 저장소 인터페이스와 구현체를 분리해 다른 저장 방식으로 교체할 수 있는 방향으로 조립 구조를 잡았습니다.
- `D`
  - 컨트롤러가 JSON 파일 구현 세부사항보다 `QuizRepository`, `StateRepository` 인터페이스에 의존합니다.

특히 중요한 점은 컨트롤러가 `"score"` 키를 직접 해석하거나, 선택지 리스트 길이를 직접 검사하지 않는다는 것입니다.

### 데메테르 원칙

데메테르 원칙은 "낯선 객체의 내부를 계속 파고들지 말고, 필요한 객체에게 직접 메시지를 보내라"는 원칙입니다.

이 프로젝트에서는 다음 방향을 지키려고 했습니다.

- `cmd == 1` 대신 `cmd.is_play_quiz()`
- 정답 비교를 위해 숫자를 꺼내 직접 비교하는 대신 `quiz.is_correct(user_answer)`
- 최고 기록 갱신 조건을 외부에서 계산하는 대신 `best_record.update(total_count, best_count)`

이렇게 하면 호출부는 "무엇을 원하는지"만 말하고, "어떻게 계산되는지"는 객체 내부에 남습니다.

### Fluent Access / 메시지 기반 접근

이 프로젝트는 getter를 무작정 늘리는 대신, 읽었을 때 의미가 드러나는 메서드를 선호합니다.

예를 들면:

- `cmd.is_exit()`
- `quiz.answer_label()`
- `best_record.summary_text()`

이런 이름은 단순히 값을 꺼내는 것보다 의도가 더 분명합니다.  
초보자 입장에서는 "객체를 데이터 통"으로 쓰는 것이 아니라 "메시지를 받는 존재"로 이해하는 데 도움이 됩니다.

## 입력 처리 흐름

사용자 입력은 다음 순서로 처리합니다.

```text
원시 문자열 입력
  -> View에서 파싱
  -> Controller에서 VO/Model 생성
  -> VO/Model 검증
  -> 실패 시 객체가 만든 에러 메시지 출력
```

예를 들어 정답 입력 흐름은 다음과 같습니다.

```python
user_input = input("\n정답 입력: ").strip()
answer_value = int(user_input)
user_answer = Answer(answer_value, quiz.choices())
```

여기서:

- `input()`과 `int()`는 View 책임
- `1~4 범위 검증`은 `Answer` 책임
- 에러 메시지도 `Answer`가 제공합니다

이 구조는 검증 로직이 View나 Controller에 흩어지는 것을 막아줍니다.

## 왜 이런 구조가 중요한가

신입 개발자가 처음 객체지향을 배울 때 가장 많이 하는 실수는 모든 값을 문자열, 숫자, 리스트로만 다루는 것입니다.  
그렇게 하면 코드가 빨리 늘어나지만, 규칙도 같이 흩어집니다.

이 프로젝트는 그 문제를 줄이기 위해 다음 원칙을 택했습니다.

- 의미 있는 값은 VO로 감싼다.
- 도메인 규칙은 Model이 직접 가진다.
- 입력, 출력, 저장은 경계 레이어로 분리한다.
- 컨트롤러는 조정자 역할만 한다.

결과적으로:

- 규칙이 한곳에 모입니다.
- 테스트 포인트가 명확해집니다.
- 수정 영향 범위가 줄어듭니다.
- 코드가 "값 나열"이 아니라 "객체 간 협력"으로 읽히게 됩니다.

이 문서를 읽을 때 가장 중요한 질문은 하나입니다.

> 이 책임은 지금 이 객체가 가져야 하는가?

이 질문을 계속 따라가면, 왜 `model`과 `vo`를 분리했고 왜 레이어를 나눴는지 자연스럽게 이해할 수 있습니다.
