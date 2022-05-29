## 关于文件传输方式的调研

此readme用来分析将音频数据从web服务器传输到算法服务器的方法。

#### 现有方法：post

我们现在使用的是post传输，数据流：采集端 -> srs(web)服务器 -> 视频/音频切片 -> 多个wav文件 -> post发送 -> 算法服务器 -> 算法。

该方法有如下缺点：

> 1. 数据需要在web服务器切片，导致web开发和算法开发需要联调。
> 2. post的时延不可靠，导致系统响应不稳定。
> 3. 多个post之间需要考虑发送顺序（现在我们采用的是串联发送）。
> 4. web端需要主动发送，对演示不求好。

#### 调研的新方法：rtmp

rtmp（real time messaging protocal），是一种基于TCP的面向直播的流媒体协议，如果采用rtmp传输，数据流将会是如下情况：采集端 -> srs(web)服务器 -> rtmp -> 算法服务器rtmp接收端 -> 音频流 -> 算法。

该方法有如下**优点**：

> 1. 全程使用音视频流，切片由算法自主控制，不需要联调。
> 2. rtmp协议稳定、延时低，延时在1-3s。
> 3. 使用音频流，不需要考虑发送顺序。
> 4. web端不需要主动发送，算法端可以通过访问指定的音频流端口，按需读取。

该方法会带来的新操作：

> 1. 需要在算法服务器部署srs
> 2. 需要算法服务器暴露1936端口
> 3. 需要算法解码m3u8流媒体数据



##### （可不看）记录一些安装步骤：

~~~bash
sudo apt install icecast
ffmpeg -re -i rtmp://localhost:1936/live/livestream -vn -ar 22050 -ac 1 -f mp3 -content_type audio/mpeg icecast://source:352648791@localhost:8000/test.mp3
~~~

