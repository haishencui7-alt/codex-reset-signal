#!/usr/bin/env python3
"""Manual GitHub Actions-only ServerChan test. No other network targets."""
import json
import os
import sys
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

key = os.getenv('SERVERCHAN_SENDKEY', '')
if not key.startswith('SCT'):
    print('ERROR: Missing ServerChan Turbo (SCT) SendKey in Actions secrets')
    sys.exit(1)
url = f'https://sctapi.ftqq.com/{key}.send'
body = urlencode({
    'title': 'Tibo 重置监控：微信通道测试',
    'desp': '这是一条人工触发的测试消息，不代表 Codex 额度已重置。',
}).encode('utf-8')
request = Request(url, data=body, method='POST', headers={
    'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
})
try:
    with urlopen(request, timeout=20) as r:
        response = json.load(r)
except HTTPError as exc:
    print(f'ERROR: ServerChan returned HTTP {exc.code}')
    sys.exit(1)
except (URLError, TimeoutError, ValueError):
    print('ERROR: ServerChan transport or JSON parsing failed')
    sys.exit(1)
if isinstance(response, dict) and response.get('code') == 0:
    print('SUCCESS: ServerChan accepted test notification. Check WeChat delivery.')
else:
    print('ERROR: ServerChan rejected test notification. Check channel and quota.')
    sys.exit(1)
