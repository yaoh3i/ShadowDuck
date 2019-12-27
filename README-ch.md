# 灰鸭
**基于HTTP短连接的完全交互式反向连接shell。**
## 特点
- 标准输入(0)、标准输出(1)、错误输出(2)不向外连接
- 标准输入(0)、标准输出(1)、错误输出(2)无管道
- 伪装成一个python爬虫
- 完全交互shell，可执行ssh/ftp等交互式命令
- 可自动重连

## 使用方法
- 修改client.py中的ip与port，修改server.py的port
- client.py基于python2.x，作用于目标机器
- server.py基于python3.x，作用于自己的服务器
- 命令前置ia可运行交互式命令，如：ia ssh root@xxx.xxx.xxx.xxx
- server端输入exit，回车即可退出。此时client进入休眠状态，每60s向server端发起请求，server端上线可恢复连接

## 警告
仅用于内网渗透防御技术研究，为防御此类攻击所用，禁止用于攻击行为，否则后果自负。