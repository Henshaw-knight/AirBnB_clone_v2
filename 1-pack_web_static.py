#!/usr/bin/python3
""" Fabric script that generates a .tgz archieve from the contents
of the web_static folder """
import os
from datetime import datetime
from fabric.api import local


def do_pack():
    """ Generates a .tgz archieve """
    current_date = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = f"web_static_{current_date}.tgz"

    # create versions folder if it doesn't exist
    if not os.path.exists("versions"):
        local("mkdir versions")

    # create the archive
    local(f"tar -czvf versions/{archive_name} web_static/")

    # check if the archive file was created
    if os.path.exists(archive_name):
        archive_path = os.path.abspath(archive_name)
        return archive_path
    else:
        return None
