#!/usr/bin/env python3
"""发送消息到飞书群并监控回复 - 使用 urllib"""
import json
import sys
import time
import urllib.request
import urllib.parse

FEISHU_APP_ID = "cli_a939f00e1478dcd2"
FEISHU_APP_SECRET = "DgDvg8XSE5BECCs97UX5uZf0BI2FpSZA"
CHAT_ID = "oc_12e40611bfbf3fad79e075b0ce4eec89"
# 排除的消息sender_id（只排除自己，不排除EC_Avatar）
EXCLUDED_SENDERS = {"cli_a939f00e1478dcd2"}
BOT_NAME = "xh1"
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
    header = f"这是来自「{BOT_NAME}」的信息"
    at_EC_Avatar = f"<at user_id=\"{EC_AVATAR_ID}\">EC_Avatar</at>"
    full_text = f"{header}\n{at_EC_Avatar}\n{text}"
    data = json.dumps({"receive_id": CHAT_ID, "msg_type": "text", "content": json.dumps({"text": full_text})}).encode()
    req = urllib.request.Request(url, data=data, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
        if result.get("code") == 0:
            return result["data"]["message_id"]
    return None

def is_our_message(msg):
    """检查是否是我们自己发的消息"""
    sender_id = msg.get("sender", {}).get("id", "")
    return sender_id == "cli_a939f00e1478dcd2"

def extract_text_content(body):
    try:
        content = json.loads(body)
        if "text" in content:
            return content["text"]
        elif "content" in content:
            if isinstance(content["content"], list):
                texts = []
                for item in content["content"]:
                    if isinstance(item, list):
                        for sub in item:
                            if sub.get("tag") == "text":
                                texts.append(sub["text"])
                return "".join(texts)
    except:
        pass
    return None

def get_messages():
    token = get_token()
    url = f"https://open.feishu.cn/open-apis/im/v1/messages?container_id_type=chat&container_id={CHAT_ID}&page_size=20&sort_type=ByCreateTimeDesc"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

def send_and_poll(message, wait_seconds=5):
    msg_id = send_message(message)
    if not msg_id:
        print("发送失败", file=sys.stderr)
        return None
    
    print(f"消息已发送: {msg_id}，等待 {wait_seconds} 秒后检查回复...", file=sys.stderr)
    time.sleep(wait_seconds)
    
    data = get_messages()
    if data.get("code") != 0:
        print("获取消息失败", file=sys.stderr)
        return []
    
    replies = []
    for msg in data.get("data", {}).get("items", []):
        # 跳过我们自己发的消息，保留其他人的（包括EC_Avatar）
        if is_our_message(msg):
            continue
        
        body = msg.get("body", {}).get("content", "")
        text = extract_text_content(body)
        
        if text:
            replies.append({
                "sender": msg.get("sender", {}).get("id", ""),
                "text": text,
                "time": msg.get("create_time", ""),
                "msg_id": msg.get("message_id", "")
            })
    
    return replies

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: send_and_poll.py <消息内容> [等待秒数]")
        sys.exit(1)
    
    message = " ".join(sys.argv[1:])
    wait = int(sys.argv[-1]) if sys.argv[-1].isdigit() else 5
    
    replies = send_and_poll(message, wait)
    
    if replies:
        print("\n=== 回复内容 ===")
        for r in replies:
            print(f"{r['text']}")
    else:
        print("\n没有找到新回复")
