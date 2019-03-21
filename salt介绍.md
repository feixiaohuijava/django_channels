# salt介绍

# <a name="kx2dxt"></a>saltstack是什么？
<span data-type="color" style="color:rgb(103, 103, 103)"><span data-type="background" style="background-color:rgb(255, 255, 255)">We’re not just talking about NaCl.</span></span>

Salt is:
* a configuration management system, capable of maintaining remote nodes in defined states (for example, ensuring that specific packages are installed and specific services are running)
* a distributed remote execution system used to execute commands and query data on remote nodes, either individually or by arbitrary selection criteria

<span data-type="color" style="color:rgb(103, 103, 103)"><span data-type="background" style="background-color:rgb(255, 255, 255)">一个配置管理系统，能够维护预定义状态的远程节点(比如，确保指定的报被安装，指定的服务在运行)</span></span>
<span data-type="color" style="color:rgb(103, 103, 103)"><span data-type="background" style="background-color:rgb(255, 255, 255)">一个分布式远程执行系统，用来在远程节点（可以是单个节点，也可以是任意规则挑选出来的节点）上执行命令和查询数据</span></span>

# <a name="vg3ekp"></a>saltstack架构
## <a name="s200gx"></a>cs架构
saltstack的架构是采用c/s架构，一个master，N个minion的方式实现的。
1它主要借助于zeromq这个中间件实现通信的，zeromq是处于网络层中的,传输层是tcp协议。它能更快的实现通讯，这个也就是比ansible更快的一个原因



![image.png | left | 720x523](https://cdn.nlark.com/yuque/0/2018/png/124258/1536764771639-ea251736-bab0-4692-acaa-44a950b1fe8b.png "")


2它依然是使用ssh进行通信验证的，在minion节点/etc/salt/pki/minion中这个文件夹中就会自动存放master节点的公钥，
 其中，它跟/root/.ssh文件夹下的机器公钥不是一致的。前者是属于saltstack组件master和minion之间的认证，后者属于机器之间的认证。
3 saltstack在Master和minion节点上都是有属于自己的守护进程的，承担着发布消息和监听端口的功能，分别是4505,4506两个端口
 4 master接受命令，将命令分发给Minion，然后minion将执行命令的结果返回给master


![2014-11-20-salt_architecture.png | center | 751x463](https://cdn.nlark.com/yuque/0/2018/png/124258/1537964404636-306cb4e0-9b06-4b23-8662-86f842d3695b.png "")


* `Salt Master` 控制中心。
* `Salt Minion` 装在被操作的服务器上。
* `Grains` 是每一台 Minion 自身的 __静态__ 属性。以 Python 字典的形式存放在 Minion 端。
* `Pillar` 存放 key-value 变量。存放在 Master 端，由 Master 编译好后，下发给 Minion。所以，可以存放密码之类的涉密的或是一些需要统一配置的变量。
* `State` 希望由 Salt 执行的一套操作。（比如 “安装 vim、配置 vim” 可以写在一个 state 里，也可以拆成两个 state 写。）执行时，Master 将 states 生成好，下发给 Minion，由 Minion 执行 states （转化成一条条命令）。

## <a name="3il6dl"></a>everything is code
saltstack能解决运维人员很多重复性的工作
1相较于传统的ssh,scp来做大规模机器同时部署操作非常方便，saltstack脚本也同样是具有幂等性。比如yum安装需要输入Y这种CLI方式就可以被saltstack避免
2saltstack利用zeromq协议在master和minion之间做消息传递，机器数量达到一定规模，saltstack实现的速度大约是ansible的40倍(网友实测例子)
3saltstack收集minion节点机器的<span data-type="color" style="color:rgb(103, 103, 103)"><span data-type="background" style="background-color:rgb(255, 255, 255)">operating system, domain name, IP address, kernel, OS type, memory, and many other system properties，利用的是saltstack的grains模块</span></span>
saltstack在master和minion安装好后，就会以daemon进程的方式存在着。

至今发现的不足：
1 需要在每个minion上配置关于master的信息
~~2 ansible能很好的解决在minion之间传输文件，但是saltstack没有，需要自己做两次scp操作（此处有误，ansible在两台remote node传输文件就使用fetch 和copy操作。以下命令是两台机器建立了ssh互信）~~
```plain
ansible: ansible src_ip -S -R root -m shell -a " scp -r src_ip:src_File tar_ip:tar_path "
```

  
# <a name="0aksdk"></a>saltstack安装
ps: saltstack官方[yum源的页面](https://mirrors.tuna.tsinghua.edu.cn/saltstack/#rhel)藏得好深~地址是指向清华的~
```
yum install https://repo.saltstack.com/yum/redhat/salt-repo-latest-2.el7.noarch.rpm 
```
使用yum命令安装，在minion节点不需要安装salt-master
* `yum install salt-master`
* `yum install salt-minion`
* `yum install salt-ssh`
* `yum install salt-syndic`
* `yum install salt-cloud`
master节点和minion节点设置开机自启：
```bash
systemctl enable salt-master.service
systemctl start salt-master.service
systemctl enable salt-minion.service
systemctl start salt-minion.service
```
在master节点配置interface,ipv6,publish\_port等：
```plain
interface: 172.17.35.239
ipv6: True
publish_port: 4505
file_roots:
  base:
     - /srv/salt/openstack-salt/base
pillar_roots:
  base:
     - /srv/salt/openstack-salt/pillar
```
在minion节点配置指向master节点:
```plain
master: 172.17.35.239
master_port: 4506
id:  controller01  #这个就是salt-key -L 中的标志

```
# <a name="xi7rxh"></a>saltstack dependencies:
可以看到的是，这里有特殊的zeromq，但是没有ansible那样的基于paramiko库
* [Python 2.7](http://python.org/download/) >= 2.7 <3.0      
* [msgpack-python](https://pypi.python.org/pypi/msgpack-python/) - High-performance message interchange format
* [YAML](http://pyyaml.org/) - Python YAML bindings
* [Jinja2](http://jinja.pocoo.org/) - parsing Salt States (configurable in the master settings)
* [MarkupSafe](https://pypi.python.org/pypi/MarkupSafe) - Implements a XML/HTML/XHTML Markup safe string for Python
* [apache-libcloud](http://libcloud.apache.org/) - Python lib for interacting with many of the popular cloud service providers using a unified API
* [Requests](http://docs.python-requests.org/en/latest) - HTTP library
* [Tornado](http://www.tornadoweb.org/en/stable/) - Web framework and asynchronous networking library
* [futures](https://github.com/agronholm/pythonfutures) - Backport of the concurrent.futures package from Python 3.2

* ZeroMQ:
    * [ZeroMQ](http://zeromq.org/) >= 3.2.0
    * [pyzmq](https://github.com/zeromq/pyzmq) >= 2.2.0 - ZeroMQ Python bindings
    * [PyCrypto](https://www.dlitz.net/software/pycrypto/) - The Python cryptography toolkit
* RAET:
    * [libnacl](https://github.com/saltstack/libnacl) - Python bindings to [libsodium](https://github.com/jedisct1/libsodium)
    * [ioflo](https://github.com/ioflo/ioflo) - The flo programming interface raet and salt-raet is built on
    * [RAET](https://github.com/saltstack/raet) - The worlds most awesome UDP protocol
# <a name="wxlbny"></a>saltstack认证
saltstack的master和minion之间同样是利用ssh进行认证的
在master节点的/etc/salt/pki/master/master.pub就是master的公钥，而在minion节点的/etc/salt/pki/minion/minion\_master.pub中就是存放master的公钥。
在master节点上，使用salt-key -L 就可查看minion的认证信息:


![image.png | left | 502x315](https://cdn.nlark.com/yuque/0/2018/png/124258/1537879441541-fe17d23e-612b-4d3a-a53f-6cd68225d62c.png "")

master节点公钥是自动分发的，如果由于minion节点某种原因导致提示unaccepted keys就得需要重新删除minion下的公钥，使用salt-key -a ip 来重新认证
# <a name="8tkqgt"></a>saltstack模块
## <a name="3kaswq"></a>saltstack脚本
saltstack脚本就是以sls为后缀的脚本，其格式本质就是yaml格式（pycharm支持sls文件格式排版，intellij idea并不支持）如果针对复杂的部署工程，就需要这种sls脚本来实现。
关于sls文件一个简单描述：
```yaml
target_a:                         # ID declaration
  state_a:                        # State declaration
    - state_func_a: some_value    # function declaration
    - state_func_b: some_value    # ...
    - state_func_c: some_value
    - require:                    # requisite declaration
      - pkg: xxx                  # requisite reference
      - file: xxx/xxx.xx
  state_b:                        # Support multiple states
    - state_parameter_a: some_value
    - state_parameter_b: some_value

target_b:
  state_x:
    - state_parameter_a: some_value
    - state_parameter_b: some_value
```

saltstack执行脚本需要在master节点配置脚本工程的目录，一般就只配两种：base和pillar
base目录代表你工程的目录，pillar代表配置文件目录
```bash
file_roots:
  base:
    - /srv/salt/openstack-salt/base
pillar_roots:
  base:
    - /srv/salt/openstack-salt/pillar

```
ps：
saltstack脚本在多个minion节点上安装软件的时候，从模板的中的配置文件传到minion节点时需要注意权限以及文件行尾符
saltstack脚本是不提供debug模式，导致需要花时间调试~
## <a name="v301pb"></a>saltstack模块
saltstack中pillar和grains是有区别的，前者指的是工程静态配置文件，后者指的是系统底层信息
```bash
salt '*' grains.ls       # 查看 grains 分类
salt '*' grains.items    # 查看 grains 所有信息
salt '*' grains.item os  # 查看 grains 某个信息
salt '*' grains.get os 

```
# <a name="dhf6pq"></a>利用saltstack脚本安装rabbitmq
在工程中配置一个rabbitmq的文件夹,对应有：
sls文件： 执行部署的sls文件
files文件： 就是模板，可以理解为rabbitmq的一些配置文件


![image.png | left | 520x253](https://cdn.nlark.com/yuque/0/2018/png/124258/1537877920199-dbc72757-1459-4876-88ee-3f96768dc427.png "")


利用yum安装erlang,rabbitmq-server组件
第一行代表任务id为rabbitmq\_install(任务id在一个sls脚本中不可以重复)
第二行代表使用saltstack的pkg.installed模块(这个是针对yum命令安装使用的)
第三、四行代表需要安装的组件为erlang和rabbitmq-server
```yaml
rabbitmq_install:
    pkg.installed:
    - pkgs:
      - erlang
      - rabbitmq-server
```
ps: saltstack并不提供模糊下载，比如vim-enhanced这个软件必须要一字不漏~

include代表先执行rabbtmq文件夹下的install.sls脚本
其中在sls脚本同样也是支持jinja格式语法的:
```
{% set rabbitmq_user = pillar['user_info']['rabbitmq'] ['rabbitmq_user'] %}
```
但是有一点要注意，yaml的注释#是不完全适合注释jinja语法，比如上面这句即便用#注释了，但是它依然会执行！


```yaml
include:                            #先执行rabbitmq下的install.sls脚本，安装erlang,rabbitmq-server
  - rabbitmq.install

rabbitmq_service:    #systemctl enable rabbitmq-server&& systemctl start rabbitmq-server
  service.running:
    - name: rabbitmq-server
    - enable: True

{% set rabbitmq_user = pillar['user_info']['rabbitmq'] ['rabbitmq_user'] %}
{% set rabbitmq_passwd = pillar['user_info']['rabbitmq'] ['rabbitmq_passwd'] %}

{% set rabbitmq_master_ip = pillar['openstack_cluster_info']['rabbitmq_master'] ['ip'] %}
{% set rabbitmq_slave_one_ip = pillar['openstack_cluster_info']['rabbitmq_slave_one'] ['ip'] %}
{% set rabbitmq_slave_two_ip = pillar['openstack_cluster_info']['rabbitmq_slave_two'] ['ip'] %}
{% set ip = salt['network.ip_addrs']('eth0')[0] %}


{% if  pillar['openstack_cluster_info']['rabbitmq_cluster']  == True and  ip in [rabbitmq_master_ip,rabbitmq_slave_one_ip,rabbitmq_slave_two_ip]  %}
add_user:
  cmd.run:
     - name: |
        rabbitmqctl add_user {{ rabbitmq_user }}  {{ rabbitmq_passwd }}
        rabbitmqctl set_permissions {{ rabbitmq_user }} ".*" ".*" ".*"
        rabbitmqctl set_user_tags {{ rabbitmq_user }} administrator
        rabbitmqctl list_users

open_rabbitmq_plugin:
  cmd.run:
     - name: |
         rabbitmq-plugins enable rabbitmq_management mochiweb webmachine rabbitmq_web_dispatch amqp_client rabbitmq_management_agent
         rabbitmq-plugins list


reload_rabbitmq_service:
  service.running:
    - name: rabbitmq-server
    - enable: True
    - reload: True
{% endif %}

```
在saltstack中，这种state api是非常多的，它支持了很多软件的安装，更多详细步骤，还请看官网:)

# <a name="8cuiig"></a>saltstack 执行
## <a name="aocxxg"></a>saltstack命令方式执行
saltstack是支持命令结果以yaml,json等格式输出的。
saltstack默认是按照highstate这种格式输出的:


![image.png | left | 826x552](https://cdn.nlark.com/yuque/0/2018/png/124258/1537881302929-1ed3a3f4-d423-46e7-b0cb-e4ef14047262.png "")

这种结果比较有点难被程序以合适的方式解析。
saltstack支持json格式输出:
```plain
salt 'controller01' state.sls demo.service --out=json --out-indent=-1
```
结果为：
```json
{"controller01": {"pkg_|-demo3_install_|-demo3_install_|-installed": {"comment": "All specified packages are already installed.", "name": "wget", "start_time": "09:17:19.848428", "result": true, "duration": 1.223, "__run_num__": 2, "changes": {}}, "pkg_|-demo1_install_|-demo1_install_|-installed": {"comment": "All specified packages are already installed.", "name": "vim-enhanced", "start_time": "09:17:18.121227", "result": true, "duration": 1037.342, "__run_num__": 0, "changes": {}}, "pkg_|-demo2_install_|-demo2_install_|-installed": {"comment": "The following package(s) were not found, and no possible matches were found in the package db: nccccc", "name": "nccccc", "start_time": "09:17:19.158723", "result": false, "duration": 689.293, "__run_num__": 1, "changes": {}}}}
```
不仅仅如此，saltstack还支持脚本执行结果存储在数据库中，mysql,redis,mongdb等

## <a name="gldefx"></a>saltstack python api
python api方式，该脚本只能在saltstack的master节点上执行
```plain
import salt.config
import salt.client

client = salt.client.LocalClient()
master = salt.config.client_config("/etc/salt/master")
cmd = client.cmd("172.17.35.247", "state.sls", ["demo.service"])
print(cmd)
```

## <a name="d997gc"></a>restapi: salt-api
其原理依然还是需要拿到token，再去请求。后续再给出demo。
# <a name="6wxgst"></a>
# <a name="6wxgst"></a>最后还会继续更新此文档，欢迎大家指出技术性的错误和saltstack新的认识 ：）

