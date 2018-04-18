# django_channels


这个工程主要是来自官网channels的文档而来的，官网是利用聊天工具的例子来实现websocket,
为避免麻烦，我就是替换了原例子
执行步骤:
python manage.py runserver 
访问127.0.0.1:8000/chat/lol/即可，
点击websocket链接，就能看到一次请求，后端有了数据自动反馈（consumer代码里可以看到是sleep的）。

后端主要是读取deploy.log的日志（deploy.sh脚本生成当前时间给
deploy.log），然后每三秒钟去看下日志是否有更新(这块暂时是利用sleep实现的)，然后读取日志反馈到前端