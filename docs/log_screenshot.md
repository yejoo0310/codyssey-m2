# 브랜치 병합 로그 기록

## 1. `feature/play-quiz` 브랜치 생성 및 병합

### 생성
```
yejoo031053822@c3r8s5 codyssey-m2 % git checkout -b feature/play-quiz
Switched to a new branch 'feature/play-quiz'
yejoo031053822@c3r8s5 codyssey-m2 % git branch
* feature/play-quiz
  main
```
![image (1).png](./images/image%20(1).png)
![image (2).png](./images/image%20(2).png)

### 병합
```
yejoo031053822@c3r8s5 codyssey-m2 % git branch
* feature/play-quiz
  main
yejoo031053822@c3r8s5 codyssey-m2 % git status
On branch feature/play-quiz
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   controller.py
        modified:   main.py
        modified:   state.json

no changes added to commit (use "git add" and/or "git commit -a")
yejoo031053822@c3r8s5 codyssey-m2 % git add .
yejoo031053822@c3r8s5 codyssey-m2 % git commit -m "feat: 퀴즈 풀기(play_quiz) 기능 구현"   
[feature/play-quiz 5bf2e24] feat: 퀴즈 풀기(play_quiz) 기능 구현
 3 files changed, 58 insertions(+), 15 deletions(-)
yejoo031053822@c3r8s5 codyssey-m2 % git checkout main
Switched to branch 'main'
Your branch is up to date with 'origin/main'.
yejoo031053822@c3r8s5 codyssey-m2 % git merge feature/play-quiz
Updating b4c2e60..5bf2e24
Fast-forward
 controller.py | 57 +++++++++++++++++++++++++++++++++++++++++++++++++++++++--
 main.py       | 14 ++------------
 state.json    |  2 +-
 3 files changed, 58 insertions(+), 15 deletions(-)
yejoo031053822@c3r8s5 codyssey-m2 % git push origin main
Enumerating objects: 9, done.
Counting objects: 100% (9/9), done.
Delta compression using up to 6 threads
Compressing objects: 100% (5/5), done.
Writing objects: 100% (5/5), 1.28 KiB | 1.28 MiB/s, done.
Total 5 (delta 4), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (4/4), completed with 4 local objects.
To https://github.com/yejoo0310/codyssey-m2.git
   b4c2e60..5bf2e24  main -> main
yejoo031053822@c3r8s5 codyssey-m2 % 
```
![image (6).png](./images/image%20(6).png)

### 로그 확인
```
yejoo031053822@c3r8s5 codyssey-m2 % git log --oneline --graph
* 49a9668 (HEAD -> feature/bonus, origin/main, refactor/cleanup, main) refactor: 출력 포맷팅 정리
* 123a8f7 refactor: state.json 최고 점수 데이터 구조 변경
* a9c6b53 refactor: 최고 기록 점수 저장 구조 개선(단순 최고 점수->상세 기록 딕셔너리)
* aebdbcb feat: 최고 점수 출력(show_best_score) 기능 구현
* f403546 feat: 저장된 퀴즈 목록 출력(view_quiz_list) 기능 구현
* 788f728 feat: 퀴즈 추가(add_quiz) 기능 구현
* 5bf2e24 (feature/play-quiz) feat: 퀴즈 풀기(play_quiz) 기능 구현
* b4c2e60 feat: JSON 파일 입출력 및 퀴즈 데이터 객체 복원 기능(load_state, save_state) 구현
* bfaf10d feat: QuizGame 클래스 정의 및 메뉴 시스템(run, show_menu) 메서드 구현
* a784228 feat: Quiz 클래스 기본 메서드(init, display, is_correct, to_dict) 구현
* 8921f76 chore: .gitignore 및 README 초기 생성
yejoo031053822@c3r8s5 codyssey-m2 % 
```
![image (5).png](./images/image%20(5).png)

---

## 2. `feature/bonus` 브랜치 생성 및 병합

### 생성
```
➜  codyssey-m2 git:(main) ✗ git checkout -b feature/bonus
Switched to a new branch 'feature/bonus'
➜  codyssey-m2 git:(feature/bonus) ✗ git branch
```


### 병합
```
➜  codyssey-m2 git:(feature/bonus) ✗ git add .
➜  codyssey-m2 git:(feature/bonus) ✗ git commit -m "feat: 힌트 보기 기능 구현 및 점수 계산 방법 변경"
[feature/bonus cf51f21] feat: 힌트 보기 기능 구현 및 점수 계산 방법 변경
 3 files changed, 129 insertions(+), 98 deletions(-)
➜  codyssey-m2 git:(feature/bonus) git switch main
Switched to branch 'main'
Your branch is up to date with 'origin/main'.
➜  codyssey-m2 git:(main) git merge --no-ff feature/bonus -m "merge: 보너스 기능 구현 브랜치 병합"
Merge made by the 'ort' strategy.
 controller.py | 172 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-----------------
 models.py     |  13 +++++++--
 state.json    | 108 ++++++++++++++++++++++++++++++++------------------------------------
 3 files changed, 207 insertions(+), 86 deletions(-)
➜  codyssey-m2 git:(main) git push origin main
Enumerating objects: 20, done.
Counting objects: 100% (20/20), done.
Delta compression using up to 8 threads
Compressing objects: 100% (16/16), done.
Writing objects: 100% (16/16), 4.53 KiB | 4.53 MiB/s, done.
Total 16 (delta 10), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (10/10), completed with 4 local objects.
To https://github.com/yejoo0310/codyssey-m2.git
   4600c09..055d40b  main -> main
➜  codyssey-m2 git:(main) 
```
![image (3).png](./images/image%20(3).png)

### 로그 확인
```
*   055d40b (HEAD -> main, origin/main, origin/HEAD) merge: 보너스 기능 구현 브랜치 병합
|\  
| * cf51f21 (feature/bonus) feat: 힌트 보기 기능 구현 및 점수 계산 방법 변경
| * 6fd27a7 feat: 모든 게임 기록 저장 기능 구현
| * 05a5c90 feat: 문제 랜덤 출제 및 문제 수 선택 기능 구현
| * 15fcfe4 feat: 퀴즈 삭제(delete_quiz) 기능 구현
|/  
* 4600c09 refactor: 퀴즈 개수가 5개 미만인 경우에도 플레이 가능하도록 예외 처리 보완
*   516b90c merge: refactor/input-validation 브랜치 병합
|\  
| * d7d8c5b (refactor/input-validation) refactor: 입력 검증 로직 공통화
|/  
* 187fb2d fix: 최고 점수 출력 f-string 구문 오류 수정
* 49a9668 refactor: 출력 포맷팅 정리
* 123a8f7 refactor: state.json 최고 점수 데이터 구조 변경
* a9c6b53 refactor: 최고 기록 점수 저장 구조 개선(단순 최고 점수->상세 기록 딕셔너리)
* aebdbcb feat: 최고 점수 출력(show_best_score) 기능 구현
* f403546 feat: 저장된 퀴즈 목록 출력(view_quiz_list) 기능 구현
* 788f728 feat: 퀴즈 추가(add_quiz) 기능 구현
* 5bf2e24 feat: 퀴즈 풀기(play_quiz) 기능 구현
* b4c2e60 feat: JSON 파일 입출력 및 퀴즈 데이터 객체 복원 기능(load_state, save_state) 구현
* bfaf10d feat: QuizGame 클래스 정의 및 메뉴 시스템(run, show_menu) 메서드 구현
* a784228 feat: Quiz 클래스 기본 메서드(init, display, is_correct, to_dict) 구현
* 8921f76 chore: .gitignore 및 README 초기 생성
(END)
```
![image (4).png](./images/image%20(4).png)


---

## 3. 트러블 슈팅

#### 문제
처음에 `feature/play-quiz` 브랜치를 병합할 땐 그냥 `git merge feature/play-quiz` 했더니 `git log --oneline --graph` 에 줄기 모양이 나타나지 않음

#### 원인
브랜치가 단순히 앞서가기만 한 상태면 `fast-forward`가 일어나서 merge commit이 안 생길 수도 있음

#### 해결
`--no -ff` merge 수행