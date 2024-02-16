#!/usr/bin/python3
# Fabric script that distributes an archive to the web_servers using do_deploy
from fabric.api import env, run, put
import os


env.user = "ubuntu"
env.hosts = ["54.144.43.187", "100.26.252.225"]


def do_pack():
    """ Generates a .tgz archive """
    current_date = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = f"web_static_{current_date}.tgz"

    if not os.path.exists("versions"):
        local("mkdir versions")

    local(f"tar -czvf versions/{archive_name} web_static/")
    if os.path.exists(archive_name):
        archive_path = os.path.abspath(archive_name)
        return archive_path
    else:
        return None


def do_deploy(archive_path):
    """ Distributes an archive to web servers """
    if not os.path.exists(archive_path):
        return False

    try:
        archive_name = archive_path.split("/")[-1]
        archive_name_with_no_ext = archive_name.split(".")[0]
        path = f"/data/web_static/releases/{archive_name_with_no_ext}/"

        # upload archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        run(f"sudo mkdir -p {path}")
        run(f"sudo tar -xzvf /tmp/{archive_name} -C {path}")
        run(f"sudo rm /tmp/{archive_name}")
        run(f"sudo mv {path}/web_static/* {path}")
        run(f"sudo rm -rf {path}web_static")
        run("sudo rm -rf /data/web_static/current")

        # Create new symbolic link
        run(f"sudo ln -s {path} /data/web_static/current")
        print("New version deployed!")
        return True
    except Exception:
        return False
