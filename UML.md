# UML

이 문서는 현재 퀴즈 게임의 구조를 UML 관점에서 정리한 문서입니다.  
Mermaid를 지원하는 Markdown 뷰어에서 다이어그램을 바로 볼 수 있습니다.

## Layer Diagram

```mermaid
flowchart TD
    Main[main.py] --> Controller[QuizGame<br/>controller.py]
    Controller --> View[ConsoleView<br/>view.py]
    Controller --> QuizRepoAbs[QuizRepository<br/>ABS]
    Controller --> StateRepoAbs[StateRepository<br/>ABS]
    QuizRepoAbs --> JsonQuizRepo[JsonFileQuizRepository]
    StateRepoAbs --> JsonStateRepo[JsonFileStateRepository]
    Controller --> QuizModel[MultipleChoiceQuiz]
    Controller --> Quizzes[Quizzes]
    Controller --> BestRecord[BestRecord]
    Controller --> VO[VOs<br/>Question / Choice / Choices / Answer / Command]

    JsonQuizRepo --> QuizJson[quiz.json]
    JsonQuizRepo --> DefaultQuizJson[default-quiz.json]
    JsonStateRepo --> StateJson[state.json]
```

## Class Diagram

관계 파악이 목적이므로, 아래 다이어그램은 각 클래스의 핵심 책임만 남기고 상세 필드와 보조 메서드는 생략했습니다.

```mermaid
classDiagram
    class QuizGame {
        +run() None
        +play_quiz() None
        +add_quiz() None
    }

    class ConsoleView {
        +show_menu() Command | None
        +show_quiz(quiz: MultipleChoiceQuiz, index: int) None
        +show_result(total_count: int, count: int, is_new_best: bool) None
    }

    class QuizRepository {
        +load() Quizzes
        +save(quizzes: Quizzes) None
    }

    class StateRepository {
        +load() BestRecord
        +save(best_record: BestRecord) None
    }

    class JsonFileQuizRepository
    class JsonFileStateRepository

    class MultipleChoiceQuiz {
        +is_correct(user_answer: Answer) bool
    }

    class Quizzes {
        +add(quiz: MultipleChoiceQuiz) None
        +is_empty() bool
        +items() list~MultipleChoiceQuiz~
    }

    class BestRecord {
        +update(total_count: int, best_count: int) bool
        +summary_text() str
    }

    class Question
    class Choice

    class Choices {
        +from_texts(texts: list[str]) Choices
    }

    class Answer {
        +label() str
        +matches(answer: Answer) bool
    }

    class Command {
        +is_play_quiz() bool
        +is_add_quiz() bool
        +is_exit() bool
    }

    QuizGame --> ConsoleView : interacts with
    QuizGame --> QuizRepository : loads/saves quizzes
    QuizGame --> StateRepository : loads/saves record
    QuizGame --> Quizzes : manages
    QuizGame --> BestRecord : updates
    QuizGame --> MultipleChoiceQuiz : creates
    QuizGame --> Question : creates
    QuizGame --> Choices : creates
    QuizGame --> Answer : creates

    JsonFileQuizRepository --|> QuizRepository
    JsonFileStateRepository --|> StateRepository
    QuizRepository --> Quizzes : persists
    StateRepository --> BestRecord : persists

    MultipleChoiceQuiz *-- Question
    MultipleChoiceQuiz *-- Choices
    MultipleChoiceQuiz *-- Answer

    Quizzes o-- MultipleChoiceQuiz
    Choices *-- Choice

    ConsoleView --> Command : parses
    ConsoleView --> Answer : parses
    ConsoleView --> MultipleChoiceQuiz : renders
    ConsoleView --> Quizzes : renders
    ConsoleView --> BestRecord : renders

    Answer --> Choices : validates with
```

## Sequence Diagram

### Quiz Solve Flow

```mermaid
sequenceDiagram
    actor User
    participant View as ConsoleView
    participant Controller as QuizGame
    participant Quiz as MultipleChoiceQuiz
    participant Record as BestRecord
    participant StateRepo as JsonFileStateRepository

    User->>View: 메뉴 입력
    View-->>Controller: Command
    Controller->>View: show_quiz_start()

    loop each quiz
        Controller->>View: show_quiz(quiz, index)
        User->>View: 정답 입력
        View->>View: int 파싱
        View-->>Controller: Answer
        Controller->>Quiz: is_correct(user_answer)
        Quiz-->>Controller: bool
        Controller->>View: 정답/오답 메시지 출력
    end

    Controller->>Record: update(total_count, best_count)
    Record-->>Controller: is_new_best
    alt new best
        Controller->>StateRepo: save(best_record)
    end
    Controller->>View: show_result(...)
```

### Add Quiz Flow

```mermaid
sequenceDiagram
    actor User
    participant View as ConsoleView
    participant Controller as QuizGame
    participant VO as Question/Choices/Answer
    participant Quiz as MultipleChoiceQuiz
    participant Quizzes as Quizzes
    participant QuizRepo as JsonFileQuizRepository

    User->>View: 새 퀴즈 원시 입력
    View->>View: 문자열/정수 파싱
    View-->>Controller: tuple(question, choices, answer)
    Controller->>VO: Question(question)
    Controller->>VO: Choices.from_texts(choices)
    Controller->>VO: Answer(answer, choices_vo)
    Controller->>Quiz: MultipleChoiceQuiz(question_vo, choices_vo, answer_vo)
    Controller->>Quizzes: add(new_quiz)
    Controller->>QuizRepo: save(quizzes)
    Controller->>View: show_quiz_saved()
```

## Notes

- `QuizGame`은 흐름 제어자이고, 입력/출력과 저장 포맷을 직접 다루지 않습니다.
- `QuizGame`은 `QuizRepository`, `StateRepository` 추상 타입에 의존하고, 실제 파일 저장은 JSON 구현체가 담당합니다.
- `ConsoleView`는 원시 입력을 파싱하지만, 정답 범위 같은 도메인 규칙은 `Answer`가 검증합니다.
- `MultipleChoiceQuiz`는 원시 문자열/숫자 묶음이 아니라 `Question`, `Choices`, `Answer`의 조합입니다.
- `Quizzes`는 퀴즈 목록을 감싸는 일급 컬렉션입니다.
- `BestRecord`는 최고 점수 계산과 갱신 규칙을 객체 내부에 캡슐화합니다.
