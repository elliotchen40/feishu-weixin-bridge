---
name: feishu-bridge
description: 飞书群与微信之间的消息桥梁。当 Elliot 说"发到飞书群"时，把消息转发到飞书群 oc_12e40611bfbf3fad79e075b0ce4eec89，并监控群消息回复，把回复内容转发到微信私聊给 Elliot。
---

# Feishu Bridge

飞书群消息转发技能，把微信→飞书群→微信的链路打通。

## 核心功能

1. **发消息到飞书群**：把 Elliot 要发到飞书群的内容发送过去
2. **监控回复**：查询飞书群最新消息，把回复内容转发到微信

## 使用场景

当 Elliot 说"发到飞书群"、"转发到飞书群"、"发到群里"时触发。

## 使用方法

### 发送消息到飞书群并监控回复

```bash
python3 ~/.openclaw/workspace/skills/feishu-bridge/scripts/send_and_poll.py "消息内容"
```

脚本会：
1. 发送消息到飞书群
2. 等待 5 秒
3. 查询飞书群最新消息（从最近一条开始往前找）
4. 提取非 bot 发送的回复
5. 打印出来供你转发到微信

### 只发送消息（不监控）

```bash
python3 ~/.openclaw/workspace/skills/feishu-bridge/scripts/send_to_feishu.py "消息内容"
```

### 只监控回复（查询最近消息）

```bash
python3 ~/.openclaw/workspace/skills/feishu-bridge/scripts/poll_replies.py
```

## 飞书群 ID

`oc_12e40611bfbf3fad79e075b0ce4eec89`

## 注意事项

- 群里有另一个 bot（`cli_a93a0689dbb91bef`）也在响应，那是另一个 bot，不是当前的 OpenClaw
- 当前 OpenClaw 的飞书 bot 是 `cli_a939f00e1478dcd2`
- 监控回复时过滤掉自己发送的消息和另一个 bot 的消息
