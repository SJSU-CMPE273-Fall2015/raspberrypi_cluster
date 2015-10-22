__author__ = 'saurabh'

from pathlib import Path
import string
import zipfile
import subprocess

import os
import random
from git import Repo
from core.models import Project
import tarfile

# Length f the dirname
N = 6

# Dict to maintain project pk to dirname
project_dictionary = {}

# Base url to store cloned project
base_path = "/home/saurabh/Desktop/"


def clone_project(project):
    """
    Method to clone remote project to local file system for building purpose.
    This can be a gitlab project or other git repository project.

    :param project:
    """
    print(project.url + ".git")
    dirname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

    project_dictionary[project.pk] = dirname
    cloned_repo = Repo.clone_from(project.url + ".git", base_path + dirname)
    print(cloned_repo)
    detect_language(project)


def find_project(project_id):
    """
    Method to fetch project from Project model based on pk.

    """
    # TODO currently fetching hard coded pk. Implement dynamic handling.
    p = Project.objects.get(pk=project_id)
    print(p)

    # TODO clone project can be removed to different manager kind of method
    clone_project(p)


def detect_language(project):
    """
    Function which detects language used for the project.
    Searches for requirements.txt for Python project and godep for GoLang project.
    :param project:
    """
    p = Path(base_path + project_dictionary[project.pk])
    if os.path.isfile(p.__str__() + '/requirements.txt'):
        print("Python Repository found..")
        download_dependencies(project)

    elif os.path.isfile(p.__str__() + '/godep.packages'):
        print("Go Repository found..")

    else:
        print("Can not identify project..")


def download_dependencies(project):
    subprocess.call(["build_manager/scripts/get_dependencies_python.sh", project_dictionary[project.pk]],
                    stdout=subprocess.PIPE)
    create_zip(project)
    pass


def remove_old_dir():
    pass


def create_zip(project):
    tar = tarfile.open(base_path + project_dictionary[project.pk] + '.tar.gz', mode='w:gz')
    try:
        # zf.write(base_path + project_dictionary[project.pk])
        path = base_path + project_dictionary[project.pk]
        for root, dirs, files in os.walk(path):
            for file in files:
                tar.add(os.path.join(root, file))

    finally:
        tar.close()
