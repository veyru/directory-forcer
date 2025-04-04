import requests
import threading
import queue
import random
import string

THREADS = 10
TIMEOUT = 3
FILTER_CODES = [404]

wordlist = [
    "admin", "login", "dashboard", "uploads", "backup.zip", "config.php",
    "user", "auth", "settings", "database", "server", "root", "data", "passwd",
    "private", "hidden", "logs", "access.log", "index.php", "home", "cpanel",
    "shell.php", "cgi-bin", "temp", "cache", "debug", "errors", "wp-admin",
    "wp-content", "wp-login.php", "backup.tar.gz", "mysql", "sql", "dump.sql",
    "mail", "support", "api", "phpmyadmin", "webmail", "admin.php",
] + [  
    ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(3, 10)))
    for _ in range(200000)
]

def brute_force(q, target_url):
    while not q.empty():
        path = q.get()
        url = f"{target_url}/{path}"
        try:
            response = requests.get(url, timeout=TIMEOUT)
            if response.status_code not in FILTER_CODES:
                print(f"Found: {url} [{response.status_code}]")
        except requests.RequestException:
            pass
        q.task_done()

def main():
    target_url = input("Enter target url: ").strip()
    if not target_url.startswith("http"):
        target_url = "http://" + target_url

    q = queue.Queue()
    for path in wordlist:
        q.put(path)

    print(f"Scanning {target_url} with {len(wordlist)} paths")

    threads = []
    for _ in range(THREADS):
        t = threading.Thread(target=brute_force, args=(q, target_url))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("Done.")

if __name__ == "__main__":
    main()
