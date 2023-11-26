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
#### Heading 4
##### Heading 5
###### Heading 6
Paragraph

<!-- Line -->
___

<!-- Text attributes -->
This is the **bold** text and this is the *italic* text and let's do ~~strikethrough~~.

<!-- Quote -->
> Don't forget to code your dream 

<!-- Bullet list -->
Fruits:
🍎
🍋

Other fruits:
🍑
🍏

<!-- Numbered list -->
Numbers:
1. first
2. second
3. third

<!-- Link -->
Click [Here](http://academy.dream-coding.com/)

<!-- Image -->
![image description](https://user-images.githubusercontent.com/61736137/102153953-b2881000-3ebb-11eb-9581-7026bc8e169e.jpg)


<!-- Table -->
|Header|Description|
|:--:|:--:|
|Cell1|Cell2|
|Cell3|Cell4|
|Cell5|Cell6|

<!-- Code -->
To print message in the console, use `console.log('your message')` and ..

```ts
console.log('hello')
```

<!-- PR Description Example -->
# What is Lorem Ipsum?
`Lorem Ipsum` is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy **text ever since the 1500s**, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

```ts
console.log('Hello World!');
```

|Feature|Description|
|--|--|
|Feature1|<img src="https://user-images.githubusercontent.com/61736137/102153953-b2881000-3ebb-11eb-9581-7026bc8e169e.jpg" width="400"><br>Feature1. Responsive Web Page|
|Feature2|<img src="https://user-images.githubusercontent.com/61736137/102153956-b451d380-3ebb-11eb-9ab7-f8bad6c05a97.png" width="400"><br>Feature2. Responsive Web Page|

## Before release
- [x] Finish my changes
- [ ] Push my commits to GitHub
- [ ] Open a pull request
