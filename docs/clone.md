# Git 저장소 복제 실습

## 별도의 로컬 디렉토리에 미션 수행 저장소 복제
```
➜  codyssey-m2 git:(main) ✗ cd ..
➜  Codyssey-2026 git:(master) ✗ git clone https://github.com/yejoo0310/codyssey-m2.git codyssey-m2-clone
Cloning into 'codyssey-m2-clone'...
remote: Enumerating objects: 101, done.
remote: Counting objects: 100% (101/101), done.
remote: Compressing objects: 100% (75/75), done.
remote: Total 101 (delta 44), reused 80 (delta 23), pack-reused 0 (from 0)
Receiving objects: 100% (101/101), 1.67 MiB | 1.06 MiB/s, done.
Resolving deltas: 100% (44/44), done.
➜  Codyssey-2026 git:(master) ✗ cd codyssey-m2-clone 
➜  codyssey-m2-clone git:(main) git remote -v
origin  https://github.com/yejoo0310/codyssey-m2.git (fetch)
origin  https://github.com/yejoo0310/codyssey-m2.git (push)
➜  codyssey-m2-clone git:(main) 
```
![image (17).png](./images/image%20(17).png)
![image (16).png](./images/image%20(16).png)
---

## 복제된 저장소에서 간단한 변경 후 commit -> push
```
➜  codyssey-m2-clone git:(main) git status
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   README.md

no changes added to commit (use "git add" and/or "git commit -a")
➜  codyssey-m2-clone git:(main) ✗ git add README.md 
➜  codyssey-m2-clone git:(main) ✗ git commit -m "docs: Git 저장소 복제 실습"
[main 91f1a82] docs: Git 저장소 복제 실습
 1 file changed, 3 insertions(+), 1 deletion(-)
➜  codyssey-m2-clone git:(main) git push origin main
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 8 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 337 bytes | 337.00 KiB/s, done.
Total 3 (delta 2), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (2/2), completed with 2 local objects.
To https://github.com/yejoo0310/codyssey-m2.git
   b2a9976..91f1a82  main -> main
➜  codyssey-m2-clone git:(main) 
```
![image (15).png](./images/image%20(15).png)

---

## 기존 로컬 작업 디렉토리에서 pull로 변경사항 가져옴
```
➜  codyssey-m2-clone git:(main) cd ../codyssey-m2
➜  codyssey-m2 git:(main) ✗ git pull origin main
remote: Enumerating objects: 5, done.
remote: Counting objects: 100% (5/5), done.
remote: Compressing objects: 100% (1/1), done.
remote: Total 3 (delta 2), reused 3 (delta 2), pack-reused 0 (from 0)
Unpacking objects: 100% (3/3), 317 bytes | 45.00 KiB/s, done.
From https://github.com/yejoo0310/codyssey-m2
 * branch            main       -> FETCH_HEAD
   b2a9976..91f1a82  main       -> origin/main
Updating b2a9976..91f1a82
Fast-forward
 README.md | 4 +++-
 1 file changed, 3 insertions(+), 1 deletion(-)
➜  codyssey-m2 git:(main) ✗ 
```
![image (14).png](./images/image%20(14).png)