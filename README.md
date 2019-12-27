# 灰鸭
**Interactive reverse connection shell based on HTTP short connection。**
[中文文档](https://github.com/TidDl3R/ShadowDuck/blob/master/README-ch.md "中文文档")
## Feature
- stdin(0), stdout(1), stderr(2) are not connected outward
- No pipeline for stdin(0), stdout(1), stderr(2)
- Pretending to be a python crawler
- Interactive shell, which can execute interactive commands such as ssh/ftp
- Automatic reconnection

## Usage
- Modify IP and port in client.py and port in server.py
- client.py is based on python2.x and is used for controlled machine
- server.py is based on python3.x and is used for your own machine
- Enter `ia` before the command to run interactive commands, such as `ia ssh root@xxx.xxx.xxx.xxx`
- Enter `exit` on the server side and press enter to exit. At this time, the client enters the sleep state and sends a request to the server every 60s. The connection can be restored when the server is online

## Warning
It is only used for the research of Intranet penetration defense technology. It is used for defense of such attacks. It is forbidden to use it for attack behavior, or the consequences will be borne by yourself.