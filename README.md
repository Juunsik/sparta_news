# sparta_news
스파르타 코딩 클럽 Django 심화 프로젝트

## 프로젝트 소개
DRF를 사용하여 긱뉴스를 참고한 스파르타 뉴스 백엔드 기능 구현하기

## 개발 기간
2024.05.03(금) ~ 2024.05.09(목)

## 개발 환경
- python 3.10
- Django 4.2
- SQLite

## 기능
- 회원가입
- 로그인
- 로그아웃
- 프로필 페이지
  - 프로필 페이지 수정
  - 패스워드 변경
- News 목록 조회
  - category 별로 정렬(News, Ask, Show, AI, Weekly)
  - 페이지네이션
- News CRUD
- 댓글 CRUD
- News 좋아요(찜하기)
- 팔로우
- AI를 사용한 News 생성

## 역할 분담
- 허준혁 - git 관리 담당, 로그아웃 프로필 구현, Ai뉴스 구현
- 임용택 - S.A 작성, 댓글 기능 구현, 팔로우 구현
- 이기배 - news 조회, 생성 구현
- 박혜진 - ERD 작성 , news 상세페이지 확인 수정, 삭제 구현, 정렬, 페이지네이션
- 이한별 - 회원가입, 로그인 구현, 좋아요 구현

## ERD

  ![](https://github.com/Juunsik/sparta_news/blob/main/News_postman/erd1.png)

## API
  [API 명세 보러가기](https://www.notion.so/4-S-A-041f754dfeb44f59b7dee3d2049c6ec9)
  
## 실행화면
- 회원가입
  
  ![](https://github.com/Juunsik/sparta_news/blob/dev/News_postman/signup.png)

----
- 프로필 페이지
  - 조건: 로그인 필수, 작성자만 조회 및 수정 가능
  - 조회
    
    ![](https://github.com/Juunsik/sparta_news/blob/dev/News_postman/profile_get.png)
    
  - 프로필 페이지 수정 & 패스워드 변경(암호화 확인을 위해 출력했지만 확인 이후 출력이 안되게 수정)
    1. description만 수정
    
       ![](https://github.com/Juunsik/sparta_news/blob/dev/News_postman/only%20description.png)

    2. description, password 수정

       ![](https://github.com/Juunsik/sparta_news/blob/dev/News_postman/both%20descriptoin%2C%20password.png)

    3. password 확인
       
       ![](https://github.com/Juunsik/sparta_news/blob/dev/News_postman/password%20not%20equal.png)

-----
- News 목록 조회
  - category 별로 정렬(News, Ask, Show, AI, Weekly)
  - 페이지네이션
    
  1. No parameter
     
     ![](https://github.com/Juunsik/sparta_news/blob/dev/News_postman/news%20list%20no%20param.png)

  2. Ask
     
     ![](https://github.com/Juunsik/sparta_news/blob/dev/News_postman/news%20list%20ask.png)

  3. Weekly
     
     ![](https://github.com/Juunsik/sparta_news/blob/dev/News_postman/news%20list%20weekly.png)

-----    
- News Create
  - 조건: 로그인 필수
  - category가 ask일 경우 url 공란 처리
  - AI를 사용한 News 생성(body 필요 없음)
 
  1. ask, ai 제외
   
     ![](https://github.com/Juunsik/sparta_news/blob/dev/News_postman/news%20create.png)

  2. ask
   
     ![](https://github.com/Juunsik/sparta_news/blob/dev/News_postman/new%20create%20ask.png)

  3. ai
  
     ![](https://github.com/Juunsik/sparta_news/blob/dev/News_postman/news%20create%20ai.png)


- News Update
  - 조건: 로그인 필수, 작성자와 로그인 유저가 같아야 함
    
  ![](https://github.com/Juunsik/sparta_news/blob/dev/News_postman/news%20update.png)

-----
- 댓글 CRUD
  - Read
    
    ![](https://github.com/Juunsik/sparta_news/blob/dev/News_postman/comments%20list.png)

  - Create
    - 조건: 로그인 필수
      
    ![](https://github.com/Juunsik/sparta_news/blob/dev/News_postman/comment%20create.png)

  - Update
    - 조건: 로그인 필수, 작성자와 로그인 유저가 같아야 함
      
    ![](https://github.com/Juunsik/sparta_news/blob/dev/News_postman/comment%20update.png)

-----
- News 좋아요(찜하기)
  - 좋아요(찜하기)
    
    ![](https://github.com/Juunsik/sparta_news/blob/dev/News_postman/like%20news.png)

  - 찜한 뉴스 목록
    
    ![](https://github.com/Juunsik/sparta_news/blob/dev/News_postman/like%20news%20list.png)

-----
- 팔로우
  
  ![](https://github.com/Juunsik/sparta_news/blob/dev/News_postman/follow.png)
  
- 팔로워
  
  ![](https://github.com/Juunsik/sparta_news/blob/dev/News_postman/follow%20list.png)
