#!/usr/bin/env python3
"""发送消息到飞书群 - 使用 urllib"""
import json
import sys
import urllib.request
import socket

FEISHU_APP_ID = "cli_a939f00e1478dcd2"
FEISHU_APP_SECRET = "DgDvg8XSE5BECCs97UX5uZf0BI2FpSZA"
CHAT_ID = "oc_12e40611bfbf3fad79e075b0ce4eec89"
BOT_NAME = socket.gethostname()
EC_AVATAR_ID = "ou_6c67f1125767e6ea5bec2bc9cf90e237"

def get_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    data = json.dumps({"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET}).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())["tenant_access_token"]

def send_message(text):
    token = get_token()
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
    at_avatar = f"<at user_id=\"{EC_AVATAR_ID}\">EC_Avatar</at>"
    header = f"信息来自容器-【{BOT_NAME}】"
    full_text = f"{header}\n{at_avatar}\n{text}"
    data = json.dumps({"receive_id": CHAT_ID, "msg_type": "text", "content": json.dumps({"text": full_text})}).encode()
    req = urllib.request.Request(url, data=data, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
        if result.get("code") == 0:
            print(f"发送成功: {result['data']['message_id']}", file=sys.stderr)
            return result["data"]["message_id"]
        else:
            print(f"发送失败: {result}", file=sys.stderr)
            return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: send_to_feishu.py <消息内容>")
        sys.exit(1)
    message = " ".join(sys.argv[1:])
    send_message(message)
