#!/usr/bin/python3
# Fabric script that distributes an archive to the web_servers using do_deploy
from fabric.api import env, run, put
import os


env.user = "ubuntu"
env.hosts = ["54.144.43.187", "100.26.252.225"]


def do_deploy(archive_path):
    """ Distributes an archive to web servers """
    if not os.path.exists(archive_path):
        return False

    try:
        archive_name = archive_path.split("/")[-1]
        archive_name_with_no_ext = archive_name.split(".")[0]
        path = "/data/web_static/releases/{}/".format(
                archive_name_with_no_ext)

        # upload archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        run("sudo mkdir -p {}".format(path))
        run("sudo tar -xzvf /tmp/{} -C {}".format(archive_name, path))
        run("sudo rm /tmp/{}".format(archive_name))
        run("sudo mv {}/web_static/* {}".format(path, path))
        run("sudo rm -rf {}web_static".format(path))
        run("sudo rm -rf /data/web_static/current")

        # Create new symbolic link
        run("sudo ln -s {} /data/web_static/current".format(path))
        print("New version deployed!")
        return True
    except Exception:
        return False
