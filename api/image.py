from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
import platform
import httpagentparser

# تنظیمات Webhook دیسکورد
WEBHOOK_URL = "https://discord.com/api/webhooks/1343686185448640553/rzowE7LMsRzHOGoN7uO1ktVkIqrkVezG2b_zsRI_kYra4JyyJildSulHQhZZ_cnvz7af"  # ❗ Webhook خود را اینجا قرار دهید

class UserLogger(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            user_agent = self.headers.get('User-Agent')
            parsed_info = httpagentparser.simple_detect(user_agent)

            user_data = {
                "سیستم‌عامل": platform.system() + " " + platform.release(),
                "مرورگر": parsed_info[1],
                "زبان مرورگر": self.headers.get('Accept-Language', 'نامشخص'),
                "منطقه زمانی": self.headers.get('Timezone', 'نامشخص')
            }

            # ارسال اطلاعات به دیسکورد
            requests.post(WEBHOOK_URL, json={
                "username": "User Logger",
                "content": "**📊 اطلاعات یک کاربر جدید دریافت شد!**",
                "embeds": [{
                    "title": "🔍 اطلاعات سیستم کاربر",
                    "color": 3447003,
                    "fields": [{"name": key, "value": f"`{value}`", "inline": False} for key, value in user_data.items()]
                }]
            })

            # ارسال پاسخ به کاربر
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(user_data, ensure_ascii=False, indent=4).encode())

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            print("خطا:", e)

# اجرای سرور
server_address = ("", 8080)  # روی پورت 8080 اجرا می‌شود
httpd = HTTPServer(server_address, UserLogger)
print("🚀 سرور در حال اجراست...")
httpd.serve_forever()
