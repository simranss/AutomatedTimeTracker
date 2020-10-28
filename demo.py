import subprocess
import re
import time
import datetime

def get_active_window_title():
    root = subprocess.Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=subprocess.PIPE)
    stdout, stderr = root.communicate()
    m = re.search(b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', stdout)
    if m != None:
        window_id = m.group(1)
        if str(window_id)[2:-1] == "0x0":
            return "Nothing"
        window = subprocess.Popen(['xprop', '-id', window_id, 'WM_NAME'], stdout=subprocess.PIPE)
        stdout, stderr = window.communicate()
    else:
        return None
    match = re.match(b"WM_NAME\(\w+\) = (?P<name>.+)$", stdout)
    if match != None:
        return match.group("name").strip(b"'b\"")
    return None


if __name__ == "__main__":
    active_window = None
    active_subtopic = None
    first = True
    start_time = None
    character_list = ["Recently Used", "Smileys & People", "Animals & Nature", "Food & Drink", "Activities", "Travel & Places", "Objects", "Symbols", "Flags", "Punctuation", "Arrows", "Bullets", "Pictures", "Currencies", "Math", "Letters"]
    while True:
        new_window = str(get_active_window_title())
        if "simran@simran-EliteBook:" in new_window:
            new_window = "Terminal"
            new_subtopic = "Terminal"
        elif re.search(".+ \[.+\]", new_window):
            ls = new_window.split("  ")
            new_subtopic = (ls[0])[2:]
            new_window = "Android Studio"
        elif "Emulator" in new_window:
            ls = new_window.split(" - ")
            new_subtopic = (ls.pop())[:-1]
            new_window = "Android Studio"
        elif new_window == "Nothing":
            new_subtopic = new_window
        else:
            ls = new_window.split(" - ")
            if len(ls) > 1:
                new_window = (ls.pop())[:-1]
                if len(ls) > 1:
                    new_subtopic = ls.pop()
                else:
                    new_subtopic = (ls.pop())[2:]
            elif (ls[0])[2:-1] in character_list:
                new_subtopic = (ls.pop())[2:-1]
                new_window = "Characters"
            else:
                new_window = (ls.pop())[2:-1]
                new_subtopic = new_window
        if active_subtopic != new_subtopic:
            if not first:
                end_time = datetime.datetime.now()
                print("end:", end_time)
                time_spent = end_time - start_time
                print("time spent:", time_spent, "\n")
            active_subtopic = new_subtopic
            active_window = new_window
            print("active window:", active_window)
            print("active subtopic:", active_subtopic)
            start_time = datetime.datetime.now()
            print("start:", start_time)
            first = False
        time.sleep(1)