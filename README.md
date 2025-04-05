# astrbot_plugin_browser


[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![AstrBot](https://img.shields.io/badge/AstrBot-3.4%2B-orange.svg)](https://github.com/Soulter/AstrBot)

## 🤝 介绍
本插件通过操控bot与浏览器交互（搜索、点击、滑动、滚动、缩放、输入、切换标签页、收藏等等），  
运行时，bot在后台打开一个浏览器，每完成一个交互动作，bot返回一张浏览器界面的截图。


## 📦 安装

### 第一步，安装本插件
直接在astrbot的插件市场搜索astrbot_plugin_browser，点击安装，等待完成即可

### 第二步，安装浏览器组件
进入astrbot的虚拟环境，安装firefox。
- Windows的示例操作
![tmp719B](https://github.com/user-attachments/assets/7a587972-fd47-41d5-bc0a-26694550be18)
- Linux的示例操作
![tmpABFB](https://github.com/user-attachments/assets/646edf2d-22fe-40ad-8876-aad285cf7aca)
- Docker的示例操作

```bash
# 打开bash来安装
sudo docker exec -it astrbot /bin/bash
pip install playwright
playwright install-deps
playwright install firefox
# 装完用exit命令退出
```
## 🤝 TODO
- 请前往插件的配置面板进行配置
  ![tmpA1B7](https://github.com/user-attachments/assets/9ca5bd1a-80fb-41cc-a9d7-acb66c841af7)
- 网站收藏夹位置如下，可打开进行自定义（后续本插件可能会新增一些管理收藏夹的指令）
  ![tmp692A](https://github.com/user-attachments/assets/d809f0f4-308f-4ad2-a555-e79ac72f3154)

## ⌨️ 使用说明
![tmp4FE5](https://github.com/user-attachments/assets/365e4a07-5ada-4f60-ac0c-c0c562d9633e)


## 📌 注意事项
1. 本插件刚发布初版，可能会存在一些意料之外的bug，欢迎提issue。
2. 想第一时间得到反馈的可以来作者的插件反馈群（QQ群）：460973561
3. 点个star支持一下呗（右上角的星星）


## 🤝 TODO
- 想办法降低性能消耗


## 📜 开源协议
本项目采用 [MIT License](LICENSE)
