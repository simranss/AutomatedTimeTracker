import subprocess
import re
import time
import datetime

def get_active_window_title():
    root = subprocess.Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=subprocess.PIPE)
    stdout, stderr = root.communicate()
    print(stdout, "\n")
    m = re.search(b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', stdout)
    print(m, "\n")
    if m != None:
        window_id = m.group(1)
        window = subprocess.Popen(['xprop', '-id', window_id, 'WM_NAME'], stdout=subprocess.PIPE)
        stdout, stderr = window.communicate()
        print(stdout, "\n")
    else:
        return None
    match = re.match(b"WM_NAME\(\w+\) = (?P<name>.+)$", stdout)
    if match != None:
        print(match, "\n")
        return match.group("name").strip(b"'\"")
    return None


if __name__ == "__main__":
    time.sleep(5)
    print(get_active_window_title(), "\n\n\n")