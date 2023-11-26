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
![image description](C:\Users\SKH\Github_local\Homepage_Design\KakaoTalk_20231126_125338741.png)
