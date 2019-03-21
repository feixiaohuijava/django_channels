# django_channels


这个工程主要是来自官网channels的文档而来的，官网是利用聊天工具的例子来实现websocket,
为避免麻烦，我就是替换了原例子
执行步骤:
python manage.py runserver 
访问127.0.0.1:8000/chat/lol/即可，
点击websocket链接，就能看到一次请求，后端有了数据自动反馈（consumer代码里可以看到是sleep的）。

后端是deploy.sh每五秒钟去deploy.log添加一行当前时间的日志，而consumers.py就是读取deploy.log日志，做到有数据增加，就反馈到页面。

