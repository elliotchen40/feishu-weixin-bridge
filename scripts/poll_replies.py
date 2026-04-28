#!/usr/bin/env python3
"""查询飞书群最新消息，过滤出回复内容 - 使用 urllib"""
import json
import sys
import urllib.request

FEISHU_APP_ID = "cli_a939f00e1478dcd2"
FEISHU_APP_SECRET = "DgDvg8XSE5BECCs97UX5uZf0BI2FpSZA"
CHAT_ID = "oc_12e40611bfbf3fad79e075b0ce4eec89"

def get_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    data = json.dumps({"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET}).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())["tenant_access_token"]

def get_messages():
    token = get_token()
    url = f"https://open.feishu.cn/open-apis/im/v1/messages?container_id_type=chat&container_id={CHAT_ID}&page_size=20&sort_type=ByCreateTimeDesc"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

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

def is_our_message(msg):
    """检查是否是我们自己发的消息"""
    sender_id = msg.get("sender", {}).get("id", "")
    return sender_id == "cli_a939f00e1478dcd2"

def poll_replies():
    data = get_messages()
    if data.get("code") != 0:
        print(f"获取消息失败: {data}", file=sys.stderr)
        return

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
    
    if replies:
        print(f"找到 {len(replies)} 条回复:", file=sys.stderr)
        for r in replies:
            print(f"[{r['sender']}] {r['text']}")
    else:
        print("没有找到新回复", file=sys.stderr)

if __name__ == "__main__":
    poll_replies()
