<!-- Heading -->
# SSL 인증서 갱신 방법 : 
## Nginx 서버 중지 -> Certbot으로 갱신 -> Nginx 서버 다시 실행 -> APP.PY run
### 1. Nginx 서버 중지:
#### Nginx 서버 제대로 종료되었는지 확인 (실행중인 nginx 있는지 확인):
```ts
taskkill /f /im nginx.exe

```
#### Nginx 서버 제대로 종료되었는지 확인 (실행중인 nginx 있는지 확인):
```ts
tasklist /fi "imagename eq nginx.exe"

```
### 2. 아래 명령을 사용하여 Certbot을 실행하고 인증서를 갱신합니다:
```ts
certbot renew
```
### 3. "certbot-nginx" 플러그인을 설치:
#### 이미 설치되어 있지 않다면 다음 명령으로 설치할 수 있습니다:
```ts
pip install certbot-nginx

```
### 4. Nginx 서버 다시 시작:
#### 인증서 갱신이 완료되면 Nginx 서버를 다시 시작합니다.
####  Nginx 설치 경로로 이동 
```ts
cd C:\nginx
```
####  Nginx 실행
```ts
nginx
```

<!-- Line -->
___


# Error Case :

>The Certificate Authority failed to download the challenge files from the temporary standalone webserver started by Certbot on port 80. Ensure that the listed domains point to this machine and that it can accept inbound connections from the internet.
**NGINX가 실행되고 있어서 발생한 문제. NGINX을 종료하고 갱신을 진행해야한다.**


<!-- Image -->
![image description](https://private-user-images.githubusercontent.com/66122916/285629626-c72d312b-8381-4711-8490-c48d1e46da1b.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTEiLCJleHAiOjE3MDA5NzQ0MDEsIm5iZiI6MTcwMDk3NDEwMSwicGF0aCI6Ii82NjEyMjkxNi8yODU2Mjk2MjYtYzcyZDMxMmItODM4MS00NzExLTg0OTAtYzQ4ZDFlNDZkYTFiLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFJV05KWUFYNENTVkVINTNBJTJGMjAyMzExMjYlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjMxMTI2VDA0NDgyMVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTM5YTc2MmQzYjNkOWY4MWFhZmEwMmY3Nzc2MzJkZmY3MmJiMzljODdkM2FmYTFiOTNlNTRhZmZkOTUxNjc3OGQmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.LZd_ZLliZLsAeWJ9-pt1eWxESLoffAceK6pfxkpFJlo)
