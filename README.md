# feishu-weixin-bridge

飞书群与微信之间的消息桥梁。让你在微信里发消息，自动转发到飞书群，并把飞书群的回复转回微信。

## 功能

- 发送消息到指定飞书群
- 自动 @EC_Avatar
- 监控飞书群回复并转回微信
- 支持添加来源 header

## 安装

### 方法一：通过 OpenClaw skill 命令安装

```bash
# 在 OpenClaw 控制台执行
openclaw skill install https://github.com/elliotchen40/feishu-weixin-bridge
```

### 方法二：手动安装

1. 克隆仓库：
```bash
git clone https://github.com/elliotchen40/feishu-weixin-bridge.git /path/to/feishu-bridge
```

2. 将 `feishu-bridge` 目录复制到你的 skills 目录：
```bash
cp -r feishu-bridge ~/.openclaw/workspace/skills/
```

## 配置

### 1. 飞书应用凭证

编辑脚本中的配置：

```python
FEISHU_APP_ID = "cli_a939f00e1478dcd2"
FEISHU_APP_SECRET = "DgDvg8XSE5BECCs97UX5uZf0BI2FpSZA"
```

> 如何获取飞书应用凭证？请参考 [飞书开放平台文档](https://open.feishu.cn/document/home/introduction-to-custom-app-development/self-built-application)

### 2. 飞书群 ID

```python
CHAT_ID = "oc_12e40611bfbf3fad79e075b0ce4eec89"
```

替换为你要使用的飞书群 ID。

### 3. EC_Avatar 的 Open ID

```python
EC_AVATAR_ID = "ou_6c67f1125767e6ea5bec2bc9cf90e237"
```

替换为你要 @ 的用户或机器人的 open_id。

### 4. 机器人名称

```python
BOT_NAME = "xh1"
```

这是显示在消息 header 中的名称，替换为你想要的任何名称。

## 使用方法

### 通过 AI 对话使用

当你说「发到飞书群 xxx」时，AI 会自动调用 `send_and_poll.py` 脚本完成发送和监控。

### 手动调用

```bash
# 发送消息并等待回复
python3 scripts/send_and_poll.py "你的消息内容"

# 只发送消息
python3 scripts/send_to_feishu.py "你的消息内容"

# 查询最近回复
python3 scripts/poll_replies.py
```

## 依赖

- Python 3.x
- 标准库（urllib, json, time）— 无需安装额外包

## 文件结构

```
feishu-weixin-bridge/
├── README.md
├── SKILL.md          # OpenClaw skill 配置
└── scripts/
    ├── send_and_poll.py    # 发送并监控回复
    ├── send_to_feishu.py   # 只发送消息
    └── poll_replies.py     # 查询回复
```

## 注意事项

- 确保机器人已被加入飞书群
- 机器人需要具有发送消息的权限
- 监控回复功能通过轮询实现，默认等待 5 秒
