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

```mermaid
classDiagram
    class QuizGame {
        -Quizzes quizzes
        -BestRecord best_record
        -ConsoleView view
        -StateRepository state_repository
        -QuizRepository quiz_repository
        -QuizRepository default_quiz_repository
        +run() None
        +create_quiz(question: str, choices: list[str], answer: int) MultipleChoiceQuiz
        +load_state() None
        +play_quiz() None
        +add_quiz() None
        +show_result(score: int) None
        +save_state() None
    }

    class ConsoleView {
        +show_menu() Command | None
        +show_quiz(quiz: MultipleChoiceQuiz, index: int) None
        +get_answer_input(quiz: MultipleChoiceQuiz) Answer | None
        +get_new_quiz_form() tuple~str, list[str], int~ | None
        +show_result(total_count: int, count: int, is_new_best: bool) None
        +show_quiz_list(quizzes: Quizzes) None
        +show_best_record(best_record: BestRecord) None
        +show_error_message(message: str) None
    }

    class QuizRepository {
        +exists() bool
        +load() Quizzes
        +save(quizzes: Quizzes) None
    }

    class StateRepository {
        +exists() bool
        +load() BestRecord
        +save(best_record: BestRecord) None
    }

    class JsonFileQuizRepository {
        -str _file_path
        +exists() bool
        +load() Quizzes
        +save(quizzes: Quizzes) None
    }

    class JsonFileStateRepository {
        -str _file_path
        +exists() bool
        +load() BestRecord
        +save(best_record: BestRecord) None
    }

    class MultipleChoiceQuiz {
        -Question _question
        -Choices _choices
        -Answer _answer
        +question() str
        +choices() Choices
        +answer() int
        +answer_label() str
        +is_correct(user_answer: Answer) bool
    }

    class Quizzes {
        +list~MultipleChoiceQuiz~ value
        +add(quiz: MultipleChoiceQuiz) None
        +count() int
        +is_empty() bool
        +has_minimum(count: int) bool
        +items() list~MultipleChoiceQuiz~
    }

    class BestRecord {
        -int _score
        -int _total_count
        -int _best_count
        +update(total_count: int, best_count: int) bool
        +has_score() bool
        +score() int
        +total_count() int
        +best_count() int
        +summary_text() str
    }

    class Question {
        +str value
    }

    class Choice {
        +str value
    }

    class Choices {
        -tuple~Choice~ _choices
        +from_texts(texts: list[str]) Choices
        +texts() list[str]
        +count() int
    }

    class Answer {
        +int value
        +label() str
        +matches(answer: Answer) bool
    }

    class Command {
        +int value
        +is_play_quiz() bool
        +is_add_quiz() bool
        +is_view_quiz_list() bool
        +is_show_best_score() bool
        +is_exit() bool
    }

    QuizGame --> ConsoleView : uses
    QuizGame --> QuizRepository : uses
    QuizGame --> StateRepository : uses
    QuizGame --> Quizzes : manages
    QuizGame --> BestRecord : manages
    QuizGame --> MultipleChoiceQuiz : creates
    QuizGame --> Question : creates
    QuizGame --> Choices : creates
    QuizGame --> Answer : creates

    QuizRepository --> Quizzes : loads/saves
    StateRepository --> BestRecord : loads/saves
    JsonFileQuizRepository --|> QuizRepository
    JsonFileStateRepository --|> StateRepository

    JsonFileQuizRepository --> Quizzes : loads/saves
    JsonFileQuizRepository --> MultipleChoiceQuiz : serializes
    JsonFileQuizRepository --> Question : creates
    JsonFileQuizRepository --> Choices : creates
    JsonFileQuizRepository --> Answer : creates

    JsonFileStateRepository --> BestRecord : loads/saves

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
