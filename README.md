## Fork 改进 (自用!!!!!)

> [TIP]
> 因为我使用的绿联Nas, 因此需要一种Docker的部署方案, 而主版本并不支持`.yaml`部署.
>
> 因此我是通过一个`python 3.11`的docker镜像来进行部署的
>
> 但是, 奇怪的是, 它的docker分卷好像有问题qwq...
>
> 因此我需要改一下代码qwq...

1. 下载`python 3.11`的docker镜像

2. 部署, 挂载:
  - `docker/Bangumi_Auto_Rename-web`:`/Bangumi_Auto_Rename-web/Bangumi_Auto_Rename-web`
  - `qb下载路径`:`/Bangumi_Auto_Rename-web/v1`
  - `视频路径`:`/Bangumi_Auto_Rename-web/v2`

3. 一键安装
```sh
echo "deb https://mirrors.aliyun.com/debian/ bullseye main non-free contrib" > /etc/apt/sources.list

apt-get update && apt-get install -y git && apt-get install -y python-is-python3

git clone https://github.com/HengXin666/Bangumi_Auto_Rename.git

pip install --upgrade pip 

apt-get install -y libnss3 libnspr4 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libatspi2.0-0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libxkbcommon0 libasound2 libpango-1.0-0 libcairo2

pip install -r requirements_docker.txt -i https://mirrors.aliyun.com/pypi/simple/

python -m src.start
```

4. 运行脚本, 添加启动项
```sh
bash ./run.sh
```

## 简介

- 😣受不了动漫剧集的命名与Emby自动刮削格式不兼容？

- 🥰本项目可以将**大部分**下载的剧集（包括动漫、电影、番剧等）转为Emby所需要的**文件结构**！

- 🚀支持剪切、复制、**硬链接（默认）**三种**移动/重命名**方式！

- ✨并且你可以通过简单的配置，让qBittorrent每次下载结束之后**自动执行转换！**

- 🥳支持复杂的目录结构！以VCB-Studio的**Re:从零开始的异世界生活**剧集合集为例：

```shell
├─[VCB-Studio] Re Zero kara Hajimeru Isekai Seikatsu
│  ├─[VCB-Studio] Re Zero kara Hajimeru Isekai Seikatsu 2nd Season [Ma10p_1080p]
│  ├─[VCB-Studio] Re Zero kara Hajimeru Isekai Seikatsu Hyouketsu no Kizuna [Ma10p_1080p]
│  ├─[VCB-Studio] Re Zero kara Hajimeru Isekai Seikatsu Memory Snow [Ma10p_1080p]
│  ├─[VCB-Studio] Re Zero kara Hajimeru Isekai Seikatsu [Ma10p_1080p]
```

可以看到大的集合里面同时包括以下**子文件夹**内容：第一季、第二季、电影冰结之绊、电影雪之回忆，而你只需要运行该程序，即可自动分门别类，**电影/番剧**会被格式化后**分别的**、正确的**复制/硬链接**到**你指定的文件夹**！

## 使用效果

![1.png](https://s2.loli.net/2024/06/26/oe8jrEg7wqdtGZ1.png)

![2.png](https://s2.loli.net/2024/06/26/8PmycWaSe3f6htC.png)

## 使用方法

### 零、申请你的TMDB_API_KEY

- 进入[官网](https://www.themoviedb.org/settings/api)申请
- 复制你的**API 密钥**，后续会用到

### 一、安装 (WEB版本)

> [!IMPORTANT] 
>
> WEB版本提高了易用性、和识别准确率, 但要求必须本机内存在git和python环境！

- 确保存在Python环境（版本需要`>=3.9`）, Git环境。
- 命令行执行
  - `git clone https://github.com/KimigaiiWuyi/Bangumi_Auto_Rename.git -b web`
  - `cd Bangumi_Auto_Rename`
  - `pip install -r requirements.txt `

- 启动
  - `python -m src.start`


![.jpg](https://s2.loli.net/2025/01/13/f56LsCtKhDm1Oky.jpg)

### 二、使用

- 打开网页之后（默认端口5999，即地址为`http://127.0.0.1:5999`）
- 先点击右上角配置按钮，将刚刚的TMDB_API填入，并且配置好各个整理路径
- 点击添加任务即可使用

### 三、在qBittorrent下载完成后自动调用该程序

> ⚠注意：箭头处的命令需要根据上面命令行自己写一下，照抄无效！（下面有提供示例）

- 打开软件，**工具** -> **设置** -> 弹出窗口中找到**下载** -> 往下滚动 -> **Torrent完成时运行**
- 根据自己的配置，写入命令，**应用**保存即可

![image.png](https://s2.loli.net/2025/02/02/GfcTiNJXs4EFDWm.png)

- 这里的命令相比于上面的命令行，需要做一些小的调整，首先一点是`path=`的输入，**一定**要用`"%F"`替换（上图可能是`%D`，那是错误的，不要关心图上的命令），这样就是每次种子实际下载的路径了
- 一个是`tag=`的输入，**可以**用`"$G"`替换，代表着创建种子时候的标签，这里如果下载的是动漫剧集，需要带上`anime`的标签，如果是电影，带上`movie`的标签，方便自动整理到对应路径，如果无任何标签，是否是电影会**自动判断**，是否是动漫则**默认为否**，如果不需要处理，可以传入`no_process`的标签
- 填入示例如下

```shell
curl -d "path="%F"&tag="%G"" http://127.0.0.1:5999/sendTask -f
```

### 四、更新

- 进入文件夹内，`cd Bangumi_Auto_Rename`
- 执行`git pull`

## 需要注意的

- 该程序依靠**TMDB API**（因为Emby也是一样的，可以保证精准度），因此对**网络环境**有一定要求！
- 该程序更加适用于动画剧集的重命名，对于电影、剧集，本身Emby的刮削足够精准了。
- 识别率并不是100%，如果有识别错误的，带上截图，提Issues！
- 该程序使用情况覆盖了很多，但是像是非常复杂的情况，例如**物语系列**这种重量级剧集（加上TMDB对于物语系列的剧集分类，非常的复杂），请不要使用本程序
- 如果已经使用了本程序刮削错误的情况，因为默认是**硬链接**模式，所以直接删除目标文件夹的对应文件即可，不会影响到源文件！
- 有任何使用上的问题或者建议都可以提Issues，尽力解答！

- 如果本插件对你有帮助，不要忘了点个Star~
- 本项目仅供学习使用，请勿用于商业用途
- [爱发电](https://afdian.com/a/KimigaiiWuyi)
- [GPL-3.0 License](https://github.com/KimigaiiWuyi/Bangumi_Auto_Rename/blob/main/LICENSE) ©[@KimigaiiWuyi](https://github.com/KimigaiiWuyi)
