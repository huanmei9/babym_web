

## 首次安装到linux

#### python环境：

1. sudo apt update
2. sudo apt upgrade
3. sudo apt-get install python3 build-essential gcc make perl dkms
4. pip3 install requests ffmpy

#### ffmpeg环境：

1. sudo rm -rf /etc/apt/sources.list
2. sudo nano /etc/apt/sources.list
3. 添加源
4. sudo apt-get update
5. sudo apt-get install ffmpeg

#### 安装并启动web服务：

1. git clone https://github.com/huanmei9/babym_web.git
2. cd babym_web/srs/trunk/
3. ./configure
4. make
5.  ./objs/srs -c conf/pc.conf

#### 虚拟机设置：

1. 添加端口映射（需要在虚拟机软件设置）：1935、1985、8081



## 在PC端安装OBS：

#### obs设置：

1. 点击"设置"-"推流"-"服务栏"-"显示全部"-"自定义"
2. 服务器栏填入: rtmp://虚拟机ip:1935/live/
3. 串流密钥填入：livestream



## 验证安装效果：

PC打开浏览器，输入：http://虚拟机ip:8081/players/srs_player.html?schema=http



如果能正常显示，则部署成功









#### 附录：

中科大源：
deb https://mirrors.ustc.edu.cn/ubuntu/ focal main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ focal main restricted universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ focal-updates main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ focal-updates main restricted universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ focal-backports main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ focal-backports main restricted universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ focal-security main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ focal-security main restricted universe multiverse
deb https://mirrors.ustc.edu.cn/ubuntu/ focal-proposed main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ focal-proposed main restricted universe multiverse
