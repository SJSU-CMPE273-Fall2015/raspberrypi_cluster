__author__ = 'saurabh'

from pathlib import Path
import string
import subprocess

import os
import random
from git import Repo
from core.models import Project, ProjectBuild
import tarfile



# Length f the dirname
N = 6

# Python slug prefix
PYTHON = "py_"

# Golang slug prefix
GOLANG = "go_"

# Dict to maintain project pk to dirname
project_dictionary = {}

# Base url to store cloned project
base_path = "/home/saurabh/Desktop/"
script_path = os.getcwd()

def find_project(project_id):
    """
    Method to fetch project from Project model based on pk.

    """
    # TODO currently fetching hard coded pk. Implement dynamic handling.
    project_id = int(project_id)
    p = Project.objects.get(pk=project_id)
    print(p)

    clone_project(p)


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


def detect_language(project):
    """
    Function which detects language used for the project.
    Searches for requirements.txt for Python project and godep for GoLang project.
    :param project:
    """
    p = Path(base_path + project_dictionary[project.pk])
    if os.path.isfile(p.__str__() + '/requirements.txt'):
        print("Python Repository found..")
        download_python_dependencies(project)

    elif os.path.isfile(p.__str__() + '/godep.packages'):
        print("Go Repository found..")
        download_go_dependencies(project)

    else:
        print("Can not identify project..")


def download_python_dependencies(project):
    """
    Download dependencies for the project.
    :param project:
    """
    subprocess.call([script_path + "/build_manager/scripts/get_dependencies_python.sh", project_dictionary[project.pk]],
                    stdout=subprocess.PIPE)
    create_zip(project, PYTHON)


def download_go_dependencies(project):
    popen = subprocess.Popen([script_path +"/build_manager/scripts/get_dependencies_golang.sh", project_dictionary[project.pk]],
                             stdout=subprocess.PIPE)
    lines_iterator = iter(popen.stdout.readline, b"")
    for line in lines_iterator:
        print(line)  # yield line

    create_zip(project, GOLANG)


def create_zip(project, language):
    """
    The function to create the slug.
    :param project:
    """

    filepath = base_path + language + project_dictionary[project.pk] + '.tar.gz'
    tar = tarfile.open(base_path + language + project_dictionary[project.pk] + '.tar.gz', mode='w:gz')
    try:
        # zf.write(base_path + project_dictionary[project.pk])
        path = base_path
        os.chdir(path)
        for root, dirs, files in os.walk(project_dictionary[project.pk]):
            for file in files:
                tar.add(os.path.join(root, file))

    finally:
        tar.close()

    update_database(project, filepath)


def update_database(project, filepath):
    project_build = ProjectBuild()
    project_build.project_id = project.id
    project_build.build.name = filepath
    project_build.save()


def remove_old_dir():
    pass
