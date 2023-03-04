import sys
import time
import signal
import subprocess


def cmdw(cmd):
    """A simple cmd wrapper."""
    print(f"[CMD] {cmd}")
    rc = subprocess.run(cmd, shell=True).returncode
    if rc != 0:
        print(f"[ERR] Could not launch: {cmd}")
        sys.exit(1)


def launch():
    """Prepare and launch the bot."""
    cmdw(f"docker build --no-cache . -t {image}")
    print(f"[NB!] Launching the {image} bot!")
    cmdw(f"docker run --rm --name {container} {image}")


def handler(signum, frame):
    """Custom SIGINT handler."""
    res = input("\n\nDo you want to stop hosting? [Y/n]: ").lower()
    if res == 'y':
        cmdw("docker rmi {image}")
        print("[NB!] Environment cleaned.")
        sys.exit(1)
    else:
        print("\n[NB!] Keeping the bot running..")


def cmdw(cmd):
    """A simple cmd wrapper."""
    print(f"[CMD] {cmd}")
    rc = subprocess.run(cmd, shell=True).returncode
    if rc != 0:
        print(f"[ERR] Could not launch: {cmd}")
        sys.exit(1)


# launch
signal.signal(signal.SIGINT, handler)
global image, container
image = "99abd-tgbot"
container = image + "-runner"
launch()
