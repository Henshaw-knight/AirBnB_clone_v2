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

    archive_name = archive_path.split("/")[-1]
    archive_name_with_no_ext = archive_name.split(".")[0]
    path = f"/data/web_static/releases/{archive_name_with_no_ext}/"

    # upload archive to the /tmp/ directory of the web server
    upload = put(archive_path, "/tmp/")

    run(f"sudo mkdir -p {path}")
    uncompress = run(f"sudo tar -xzvf /tmp/{archive_name} -C {path}")
    archive_deletion = run(f"sudo rm -rf /tmp/{archive_name}")
    run(f"sudo mv {path}/web_static/* {path}")
    run(f"sudo rm -rf {path}/web_static")
    symlink_deletion = run("sudo rm /data/web_static/current")

    # Create new symbolic link
    new_symlink = run(f"sudo ln -s {path} /data/web_static/current")

    if (upload.succeeded and uncompress.succeeded and
            archive_deletion.succeeded and
            symlink_deletion.succeeded and new_symlink.succeeded):
        print("New version deployed!")
        return True
    else:
        return False
