# Machbase Neo Windows service

`machbase-neo service` 명령은 Windows 서비스 등록을 제어합니다. 서비스 설치가 끝나면 Windows 부팅과 함께 machbase-neo가 자동으로 시작됩니다.

> **Note**  
> 이 작업들은 **관리자** 권한이 필요합니다.

## machbase-neo service install

machbase-neo를 Windows 서비스에 등록합니다.

```cmd
machbase-neo.exe service install --host 0.0.0.0 --data D:\database --file D:\database\files --log-filename D:\database\machbase-neo.log
```

## machbase-neo service remove

machbase-neo를 Windows 서비스에서 제거합니다.

```cmd
machbase-neo.exe service remove
```

## 시작과 중지

서비스 프로세스를 시작하고 중지합니다. Windows 서비스 제어판이 제공하는 동작과 같습니다.

```cmd
machbase-neo.exe service start
```

```cmd
machbase-neo.exe service stop
```
