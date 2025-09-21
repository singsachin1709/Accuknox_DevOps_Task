import requests
import datetime


applications = [
    "https://devopstutorial.xyz",  
    "https://www.devopstutorial.xyz"
]


LOG_FILE = "app_health.log"

def log_status(url, status):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"{timestamp} - {url} is {status}"
    print(message)
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")

def check_application(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            log_status(url, "UP")
        else:
            log_status(url, f"DOWN (HTTP {response.status_code})")
    except requests.RequestException as e:
        log_status(url, f"DOWN (Error: {e})")

if __name__ == "__main__":
    for app in applications:
        check_application(app)

