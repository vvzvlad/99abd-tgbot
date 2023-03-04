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
    cmdw(f"docker run --rm -d --name {container} {image}")
    # this is pretty bad, but also does the job
    print("[NB!] Bot is running!")
    print("[NB!] Logs are below..")
    cmdw(f"docker logs --follow {container}")


def handler(signum, frame):
    """Custom SIGINT handler."""
    res = input("\n\n[ ? ] Do you want to stop hosting? [Y/n]: ").lower()
    if res == 'y':
        print("\n[NB!] Cleaning the environment..")
        cmdw(f"docker stop {container}")
        # need a short window to actually kill the container
        time.sleep(1)
        cmdw(f"docker rmi {image}")
        print("[NB!] Done!\n")
        sys.exit(1)
    else:
        print("\n[NB!] Keeping the bot running..")
        cmdw(f"docker logs --follow {container}")


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
