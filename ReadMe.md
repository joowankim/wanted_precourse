# Bulletin Board

## Required Functions

1. 글 작성
2. 글 확인
3. 글 목록 확인
4. 글 수정
5. 글 삭제

6. 유저 생성
7. 유저 인증
8. 유저 인가

### 제약사항

1. 글에 대한 Delete와 Update는 해당 글을 쓴 유저만 가능
2. Read는 pagination 구현 필수
3. 데이터베이스는 in-memory db로 구현
4. unit test 가산점

## User Stories

1. 작가는 글을 작성할 수 있다.
2. 작가는 자신이 작성한 글만 삭제할 수 있다.
3. 작가는 다른 작가가 작성한 글은 삭제할 수 없다.
4. 작가는 자신이 작성한 글만 수정할 수 있다.
5. 작가는 다른 작가가 작성한 글은 수정할 수 없다.

6. 유저는 글 목록을 확인할 수 있습니다.
7. 유저는 글을 확인할 수 있습니다.
8. 유저는 로그인을 할 수 있습니다.
9. 유저는 회원가입을 할 수 있습니다.

## Ubiquitous Language

1. 글(Post)
2. 작가(Author)
3. 유저(User)
4. 작성하다(write)
5. 삭제하다(delete)
6. 수정하다(update)
7. 확인하다(read)
8. 인증하다(authenticate)
9. 인가하다(authorize)
