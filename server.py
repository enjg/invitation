#!/usr/bin/env python3
"""简易HTTP服务器，支持 /1 /2 /3 路由"""
import http.server
import os

IMG_MAP = {
    "1": "https://oa.fancychina.net:9000/ycyh/20260525/ed731e124751b1f8681a2a0f73c78f82_1779679073279.jpg",
    "2": "https://oa.fancychina.net:9000/ycyh/20260525/1_1779679290521.jpg",
    "3": "https://oa.fancychina.net:9000/ycyh/20260525/2_1779679318716.jpg",
}

HTML_TEMPLATE = open("/home/ubuntu/invite/index.html", "r").read()

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # 静态文件
        if self.path == '/bgm.mp3':
            self.send_response(200)
            self.send_header("Content-Type", "audio/mpeg")
            self.end_headers()
            with open("/home/ubuntu/invite/bgm.mp3", "rb") as f:
                self.wfile.write(f.read())
            return
        path = self.path.strip("/")

        # 路由: /1, /2, /3
        if path in IMG_MAP:
            if not IMG_MAP[path]:
                # 图片链接还没填，显示占位
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"""<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>待配置</title><style>body{{margin:0;height:100vh;display:flex;align-items:center;justify-content:center;background:#111;color:#fff;font-family:sans-serif;font-size:18px;}}</style></head>
<body><p>第 {path} 页 — 图片链接待配置</p></body></html>""".encode())
                return

            # 替换图片链接，返回HTML
            html = HTML_TEMPLATE.replace(
                "IMG_URL_PLACEHOLDER",
                IMG_MAP[path]
            )
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode())
            return

        # 默认: / 或其他 → 显示链接列表
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        links = ""
        for k, v in IMG_MAP.items():
            status = "✅ 已配置" if v else "⏳ 待配置"
            links += f'<p><a href="/{k}" style="color:#fff;font-size:20px;">第{k}页</a> — {status}</p>'
        self.wfile.write(f"""<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>邀请函</title><style>body{{margin:0;height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;background:#111;color:#fff;font-family:sans-serif;}}
a{{text-decoration:none;transition:opacity 0.2s;}}a:hover{{opacity:0.7;}}</style></head><body>{links}</body></html>""".encode())

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    # 把模板中的图片URL占位
    os.chdir("/home/ubuntu/invite")
    server = http.server.HTTPServer(("0.0.0.0", 8888), Handler)
    print("Server running on port 8888")
    server.serve_forever()
