import subprocess

def start(tmp_list, tablename):
    subprocess.Popen(["tmux", "new", "-d", "python3.9", "search.py", tmp_list, sys.argv[1]]).communicate()
