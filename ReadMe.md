# Bulletin Board

## 애플리케이션 구조

최상위 디렉토리의 구조는 `src`와 `tests` 디렉토리, 그리고 `pyproject.toml`을 포함하고 있습니다.
- `src`: 애플리케이션의 구현 코드를 포함하고 있습니다.
- `tests`: 애플리케이션의 테스트 코드를 포함하고 있습니다.
- `pyproject.toml`: 본 프로젝트는 `poetry`를 이용해 패키지 의존성을 관리하며 이를 위해 `.toml` 파일을 사용합니다.

### `src`

해당 애플리케이션은 `Member`, `Post`, `Security`라는 3가지 경계으로 나뉘어 있습니다. 
그리고 각 경계내부는 `router`(controller), `application`(service), `domain`, `infra` 계층으로 구성되어 있습니다.

- `router.py`: 각 경계로 들어오는 요청을 인가하고 application 계층으로 전달하는 역할을 가집니다.
- `application`: 들어온 요청의 데이터를 domain 계층의 모델로 정제하고 도메인 모델이 요청을 수행하도록 이를 호출합니다.
- `domain`: 들어온 요청을 비즈니스 규칙으로 처리합니다.
- `infra`: repository를 추상화하여 domain이 저장소에 접근할 수 있는 인터페이스를 제공합니다. 또한, 추상화된 인터페이스를 구현한 구현체를 이용해 영속성 저장소와 직접적으로 소통합니다.

### `tests`

테스트 코드는 영속성 저장소와의 커넥션을 테스트하는 코드를 포함하는 `integration` 디렉토리와 구현 코드의 각 컴포넌트를 테스트하는 `unit` 디렉토리로 구성되어 있습니다.

## 사용 방법

### 어플리케이션 실행 방법

1. `git`과 `Docker`, `Docker Compose`를 설치합니다.
    - [git 설치 가이드 url](https://git-scm.com/book/ko/v2/%EC%8B%9C%EC%9E%91%ED%95%98%EA%B8%B0-Git-%EC%84%A4%EC%B9%98)
    - [Docker 설치 가이드 url](https://docs.docker.com/engine/install/)
    - [Docker Compose 설치 가이드 url](https://docs.docker.com/compose/install/)
2. 해당 레포지토리를 클론합니다.
    ```bash
     $ git clone https://github.com/joowankim/wanted_precourse.git
    ```
3. 레포지토리를 클론한 위치에서 도커 컨테이너를 빌드하고 실행합니다.
    ```bash
    $ docker-compose up
    ```
4. `http://localhost:8000` 이후에 아래 Endpoint를 추가해 api를 호출합니다.

### Endpoint 호출 방법

해당 애플리케이션의 endpoint는 다음의 7개입니다.

- `GET /posts`
- `POST /posts`
- `GET /posts/{post_id}`
- `DELETE /posts/{post_id}`
- `PATCH /posts/{post_id}`
- `POST /members`
- `POST /security/login`

#### Post

게시물을 관리하는 Endpoints입니다. 각 게시물은 `post_id`, `author`, `title`, `content` 항목을 포함합니다.

##### `GET /posts`

해당 Endpoint는 모든 게시물을 반환합니다. 
하지만 모든 게시물을 한번에 불러오진 않으며 `page`와 `size` QueryParameters를 이용해 그 개수를 조절할 수 있습니다.


###### 요청 방법

QueryParam

- `page`: 페이지의 번호를 의미합니다. 1페이지는 100개의 게시물로 이루어집니다.
- `size`: 불러오려는 게시물의 개수입니다. 최소 1개부터 최대 100개까지 불러올 수 있습니다.

사용 예

```commandline
$ curl -X 'GET' \
      'http://localhost:8000/posts?page=1&size=50' \
      -H 'accept: application/json'
```

반환 예
```
{
  "items": [
    {
      "post_id": "post-0f0efc5e-f34f-4f77-b93e-ca5f5d1f9644",
      "author": "asdf",
      "title": "qweasdqweda",
      "content": "123qweads"
    },
    {
      "post_id": "post-7cca6d2a-5f7b-4b41-98e1-75bf6475100a",
      "author": "asdf",
      "title": "qweasdqweda",
      "content": "123qweads"
    }
  ],
  "total": 2,
  "page": 1,
  "size": 50
}
```

##### `POST /posts`

게시물을 생성합니다. 
게시물을 생성하는 작업은 인가된 사용자만 가능하여 요청에 `Authorization` 헤더를 추가하여 액세스 토큰을 입력하도록 요구합니다.

###### 요청 방법

request header

- `Authorization`: 액세스 토큰을 의미합니다.

request body(json)

- `title`: 게시물의 제목을 의미합니다.
- `content`: 게시물의 내용을 의미합니다.

사용 예
```commandline
curl -X 'POST' \
  'http://localhost:8000/posts' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuaWNrbmFtZSI6ImFzZGYifQ.2IE__EFDsKod_3MaV5XSYMaVyvAPFX-P-GxOfTKvf80' \
  -d '{
  "title": "string",
  "content": "string"
}'
```

반환 예

```
Response Code: 201 Created
```

##### `GET /posts/{post_id}`

특정 id의 게시물을 가져옵니다.

###### 요청 방법

PathParam

- `post_id`: 게시물의 식별자입니다.

요청 예

```commandline
curl -X 'GET' \
  'http://localhost:8000/posts/post-0f0efc5e-f34f-4f77-b93e-ca5f5d1f9644' \
  -H 'accept: application/json'
```

반환 예

```
Response Code: 200 OK

Response Body:
{
  "post_id": "post-0f0efc5e-f34f-4f77-b93e-ca5f5d1f9644",
  "author": "asdf",
  "title": "qweasdqweda",
  "content": "123qweads"
}
```

##### `DELETE /posts/{post_id}`

게시물을 삭제합니다.
해당 게시물의 작가가 아니라면 요청은 실패합니다.

###### 요청 방법

request header

- `Authorization`: 액세스 토큰을 의미합니다.

PathParam

- `post_id`: 게시물의 식별자입니다.

사용 예

```commandline
curl -X 'DELETE' \
  'http://localhost:8000/posts/post-0f0efc5e-f34f-4f77-b93e-ca5f5d1f9644' \
  -H 'accept: */*'
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuaWNrbmFtZSI6ImFzZGYifQ.2IE__EFDsKod_3MaV5XSYMaVyvAPFX-P-GxOfTKvf80'
```

반환 예

```
Response Code: 204 No Content
```

##### `PATCH /posts/{post_id}`

게시물의 제목이나 내용을 수정합니다.
게시물의 작가만 수정할 수 있습니다.

###### 요청 방법

request header

- `Authorization`: 액세스 토큰을 의미합니다.

PathParam

- `post_id`: 게시물의 식별자입니다.

사용 예

```commandline
curl -X 'PATCH' \
  'http://localhost:8000/posts/post-7cca6d2a-5f7b-4b41-98e1-75bf6475100a' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuaWNrbmFtZSI6ImFzZGYifQ.2IE__EFDsKod_3MaV5XSYMaVyvAPFX-P-GxOfTKvf80' \
  -d '{
  "title": "string",
  "content": "string"
}'
```

반환 예

```
Response Code: 200 OK
```

#### Member

사용자의 생성과 같은 작업을 처리하기 위한 Endpoints입니다.

##### `POST /members`

사용자를 생성합니다.

###### 요청 방법

request body(json)

- `nickname`: 유저의 아이디입니다. 중복되는 아이디는 허용하지 않습니다.
- `password`: 비밀번호 입니다.

요청 예

```commandline
curl -X 'POST' \
  'http://localhost:8000/members' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "nickname": "asdf",
  "password": "1111"
}'
```

반환 예

```
Response Code: 200 OK
```

#### Security

사용자의 인증/인가를 처리하는 Endpoints입니다.

##### `POST /security/login`

사용자를 인증합니다.
인증된 요청에는 `auth`라는 이름의 액세스 토큰을 반환합니다.

###### 요청 방법

request body(json)

- `nickname`: 유저의 아이디입니다.
- `password`: 비밀번호 입니다.

요청 예
```commandline
curl -X 'POST' \
  'http://localhost:8000/security/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "nickname": "asdf",
  "password": "1111"
}'
```

반환 예
```
Response Code: 200 OK

Response Body:
{
  "auth": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuaWNrbmFtZSI6ImFzZGYifQ.2IE__EFDsKod_3MaV5XSYMaVyvAPFX-P-GxOfTKvf80"
}
```

