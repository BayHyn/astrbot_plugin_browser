
<div align="center">

![:name](https://count.getloli.com/@astrbot_plugin_QQAdmin?name=astrbot_plugin_QQAdmin&theme=minecraft&padding=6&offset=0&align=top&scale=1&pixelated=1&darkmode=auto)

# astrbot_plugin_QQAdmin

_✨ [astrbot](https://github.com/AstrBotDevs/AstrBot) QQ群管插件 ✨_  

[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![AstrBot](https://img.shields.io/badge/AstrBot-3.4%2B-orange.svg)](https://github.com/Soulter/AstrBot)
[![GitHub](https://img.shields.io/badge/作者-Zhalslar-blue)](https://github.com/Zhalslar)

</div>

## 🤝 介绍

- 本插件利用Onebot协议接口，实现了QQ群的各种管理功能，旨在帮助用户更方便地管理群聊。  
- 功能包括：禁言、全体禁言、踢人、拉黑、改群昵称、改头衔、设管理员、设精华、撤回消息、改群头像、改群名、发群公告等等。
- 同时本插件实现了权限控制：超级管理员 > 群主 > 管理员 > 成员。

## 📦 安装

- 可以直接在astrbot的插件市场搜索astrbot_plugin_QQAdmin，点击安装，耐心等待安装完成即可  

- 或者可以直接克隆源码到插件文件夹：

```bash
# 克隆仓库到插件目录
cd /AstrBot/data/plugins
git clone https://github.com/Zhalslar/astrbot_plugin_QQAdmin

# 控制台重启AstrBot
```

## ⌨️ 使用说明

![tmp9A19](https://github.com/user-attachments/assets/3ecd3121-aa38-4bf5-b0e9-566b96237008)

## 🤝 配置

进入插件配置面板进行配置

- 可自定义超级管理员名单（这里的超管不是全局超管，而是仅仅针对本插件而言）
- 所有命令都可以自定义使用者的身份等级：超级管理员 > 群主 > 管理员 > 成员
- 可自定义随机禁言的时长范围
![tmp1872](https://github.com/user-attachments/assets/39eb983d-7eb0-4df7-a8b7-1f5fb8f7eef0)

## 🤝 TODO

- [x] 权限控制
- [x] 禁言、解禁、随机禁言、全体禁言、解除全体禁言
- [x] 踢人、拉黑
- [x] 改群昵称、改头衔
- [x] 设置管理员、取消管理员
- [x] 撤回指定消息
- [x] 改群头像、改群名
- [x] 发布群公告、删除群公告
- [x] 定时宵禁
- [x] 违禁词撤回并禁言
- [ ] 进群审批
- [ ] 群文件管理

## 👥 贡献指南

- 🌟 Star 这个项目！（点右上角的星星，感谢支持！）
- 🐛 提交 Issue 报告问题
- 💡 提出新功能建议
- 🔧 提交 Pull Request 改进代码

## 📌 注意事项

- 本插件目前仅测试了napcat协议端，其他协议端可能会存在一些不兼容问题（以具体情况为准）
- 想第一时间得到反馈的可以来作者的插件反馈群（QQ群）：460973561
