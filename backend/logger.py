import os
from datetime import datetime

def log_request(url):
    print(f"[{datetime.now()}] PID: {os.getpid()} | URL analyzed: {url}")
