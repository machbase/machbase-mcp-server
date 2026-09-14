# Machbase Neo Linux service

*systemd*나 *supervisord*를 사용하면 machbase-neo 프로세스를 시스템 서비스로 실행·관리할 수 있어 시스템 부팅 시 자동으로 시작됩니다.

## 시작/중지 스크립트 작성

**neo-start.sh 작성**

```sh
$ vi neo-start.sh
```

```sh
#!/bin/bash 
exec /data/machbase-neo serve --host 0.0.0.0 --log-filename /data/log/machbase-neo.log
```

```sh
$ chmod 755 neo-start.sh
```

**neo-stop.sh 작성**

```sh
$ vi neo-stop.sh
```

```sh
#!/bin/bash 
/data/machbase-neo shell shutdown
```

```sh
$ chmod 755 neo-stop.sh
```

## systemd

### 1단계: neo.service 작성

```sh
$ cd /etc/systemd/system
$ sudo vi neo.service
```

```ini
[Unit]   
Description=neo service   
StartLimitBurst=10   
StartLimitIntervalSec=10   
  
[Service]   
User=machbase   
LimitNOFILE=65535   
ExecStart=/data/neo-start.sh
ExecStop=/data/neo-stop.sh
ExecStartPre=sleep 2   
WorkingDirectory=/data   
Restart=always   
RestartSec=1   
  
[Install]   
WantedBy=multi-user.target   
```

* 환경에 맞게 `User`와 경로를 수정하세요.

### 2단계: 서비스 활성화

```sh
$ sudo chmod 755 neo.service
$ sudo systemctl daemon-reload
```

호스트 장비가 재부팅될 때 서비스가 자동 시작되도록 설정합니다.

```sh
$ sudo systemctl enable neo.service
```

### Step 3: Done

서비스를 활성화한 뒤 다음 명령으로 제어할 수 있습니다:

```sh
$ sudo systemctl start neo.service
$ sudo systemctl status neo.service
$ sudo systemctl stop neo.service
```

## supervisord

### 1단계: neo.conf 작성

```sh
$ cd /etc/supervisor/conf.d
$ sudo vi neo.conf
```

```ini
[program:neo]
command=/data/neo-start.sh
priority=10   
autostart=true   
autorestart=true   
environment=HOME=/home/machbase   
stdout_logfile=/data/log/machbase-neo_stdout.log   
stderr_logfile=/data/log/machbase-neo_stderr.log   
user=machbase   
```

* 환경에 맞게 `user`와 경로를 수정하세요.
* 위 예제에서 로그 폴더 `/data/log`가 미리 있어야 합니다.

### 2단계: Supervisord 갱신

```sh
$ sudo supervisorctl reread
$ sudo supervisorctl update
```

### Step 3: Done

서비스를 활성화한 뒤 다음 명령으로 machbase-neo를 제어할 수 있습니다:

```sh
$ sudo supervisorctl start neo
$ sudo supervisorctl status neo
$ sudo supervisorctl stop neo
```

## PM2

### 1단계: neo-start.sh 작성

```sh
$ vi neo-start.sh
```

```sh
#!/bin/bash
exec /data/machbase-neo serve --host 0.0.0.0
```

* 로그는 PM2가 관리하므로 `--log-filename` 옵션은 필요 없습니다.

### 2단계: neo-start.sh 실행 권한 부여

```sh
$ chmod 755 neo-start.sh
```

### 3단계: PM2로 machbase-neo 실행

```sh
$ pm2 start /data/neo-start.sh --name neo --log /data/log/machbase-neo.log
```

machbase-neo의 상태를 확인합니다.

```sh
$ pm2 status neo
```

### 4단계: PM2 자동 시작 설정

* 이미 실행했다면 이 과정은 건너뛰어도 됩니다.

시작 스크립트를 자동으로 생성·설정하려면 (sudo 없이) `pm2 startup` 명령을 입력합니다:

```sh
$ pm2 startup
[PM2] Init System found: systemd
[PM2] To setup the Startup Script, copy/paste the following command:
sudo env PATH=$PATH:/usr/local/bin /usr/local/lib/node_modules/pm2/bin/pm2 startup systemd -u machbase --hp /home/machbase
```

그리고 표시된 명령을 터미널에 복사해 붙여넣습니다:

```sh
$ sudo env PATH=$PATH:/usr/local/bin /usr/local/lib/node_modules/pm2/bin/pm2 startup systemd -u machbase --hp /home/machbase
```

이제 PM2가 부팅 시 자동으로 재시작합니다.

### 5단계: 앱 목록 저장

원하는 앱을 모두 시작한 뒤, 재부팅 후에도 다시 실행되도록 앱 목록을 저장합니다:

```sh
$ pm2 save
```

### Step 6: Done

다음 명령으로 machbase-neo를 제어할 수 있습니다:

```sh
$ pm2 start neo
$ pm2 status neo
$ pm2 stop neo
$ pm2 restart neo

$ pm2 logs neo
$ pm2 monit
```
