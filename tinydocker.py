import os
import sys
import time
import signal
import subprocess


def recipe_generate():
    """Generate a Dockerfile to build a primitive image."""
    contents = """
FROM python:3-slim

# prepare environment
WORKDIR /app
COPY . /app
RUN python3 -m pip install -r requirements.txt

# setup CMD
CMD [ "python3", "app.py" ]
    """
    # delete potential old recipe and generate a new one
    if dockerfile in os.listdir():
        os.remove(dockerfile)
    with open(dockerfile, "w") as f:
        # exclude first line because it's empty anyway
        f.write("\n".join(contents.splitlines()[1:]))


def cmdd(cmd):
    """A simple (Docker) command wrapper."""
    print(f"[CMD] {cmd}")
    rc = subprocess.run(cmd, shell=True).returncode
    if rc != 0:
        print(f"[ERR] Could not launch: {cmd}")
        sys.exit(1)


def launch():
    """Prepare and launch the bot."""
    cmdd(f"docker build --no-cache -f {dockerfile} . -t {image}")
    os.remove(dockerfile)
    cmdd(f"docker run --rm -d --name {container} {image}")
    print("[NB!] Bot is running!")
    print("[NB!] Logs are below..")
    # start monitoring logs
    cmdd(f"docker logs --follow {container}")


def handler(signum, frame):
    """Custom SIGINT handler."""
    res = input("\n\n[ ? ] Do you want to stop hosting? [Y/n]: ").lower()
    if res == 'y':
        print("\n[NB!] Cleaning the environment..")
        cmdd(f"docker stop {container}")
        # need a short time window to actually remove the container
        time.sleep(1)
        cmdd(f"docker rmi {image}")
        print("[NB!] Done!\n")
        sys.exit(1)
    else:
        print("\n[NB!] Keeping the bot running..")
        # keep monitoring logs
        cmdd(f"docker logs --follow {container}")


# launch
signal.signal(signal.SIGINT, handler)
global dockerfile, image, container
dockerfile = "Dockerfile"
image = "99abd-tgbot"
container = image + "-runner"
recipe_generate()
launch()
