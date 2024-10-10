"""Module for create function for BCT CLI"""

import json 
from PyInquirer import prompt
import subprocess
import os
import platform
import requests


def get_templates():
    config_abs_path = os.path.join(os.path.dirname(__file__), 'config.json') 
    with open(config_abs_path, 'r') as f: 
        config_content = json.load(f) 

    if config_content["localUrlJson"]:
        template_abs_path = config_content["templateUrlPath"]
        return read_templates(template_abs_path)
    else: 
        template_url = config_content["templateUrlApi"]
        my_data = requests.get(template_url)
        return my_data.json()


def read_templates(json_address: str) -> dict: 
    with open(json_address, 'r') as file: 
        data = json.load(file) 
    return data


def create(): 
    template_dict = get_templates()
    branch_name_message = 'Please input a name for the local branch (master by default). \n If you are syncing with \
        an existing bitbucket repository, please name the branch according to the one you wish to track in the \
        bitbucket repository!!'
    questions = [
        {
                'type': 'list',
                'name': 'template',
                'choices': template_dict.keys(),
                'message': 'Please choose the template you want to use',
        },         
        {
                'type': 'input',
                'name': 'projectName',
                'message': 'Please input the project name',
                'default': 'my-project',
        },
        {
                'type': 'input',
                'name': 'bitbucketProjectUrl',
                'message': 'Please input the bitbucket project url',
        }, 
        {
                'type': 'input',
                'name': 'branchName',
                'message': branch_name_message, 
                'default': 'master'
        }
    ]   

    answers = prompt(questions)
    template = answers['template']
    project_name = answers['projectName']
    bitbucket_url = answers['bitbucketProjectUrl']
    branch_name = answers['branchName']

    template_url = template_dict[template]
    clone_template_call = 'git clone ' + template_url + ' ' + project_name + ' --depth=1'

    subprocess.run(clone_template_call, shell=True)

    delete_git_dir(project_name)

    project_path = os.path.join(os.path.dirname(__file__), project_name)
    print(project_path)

    if bitbucket_url == '': 
        print('Cloning successful!')
    else: 
        git_init = 'git init'
        git_rename = 'git branch -m {}'.format(branch_name)
        git_remote_add_origin = 'git remote add origin ' + bitbucket_url
        git_set_upstream = 'git fetch --set-upstream origin {}'.format(branch_name)
        git_pull = 'git pull'

        subprocess.run(git_init, cwd=project_path)
        subprocess.run(git_remote_add_origin, cwd=project_path)
        subprocess.run(git_rename, cwd=project_path)
        subprocess.run(git_set_upstream, cwd=project_path)
        subprocess.run(git_pull, cwd=project_path)


def delete_git_dir(project_name):
    sys_type = platform.system()
    git_folder_path = '"' + os.path.join(project_name, '.git') + '"'
    print('Git folder path:', git_folder_path)
    if sys_type == 'Windows':
        delete_git = 'rmdir /S /Q ' + git_folder_path
    else:
        delete_git = 'rm -rf ' + git_folder_path
    subprocess.run(delete_git, shell=True)


if __name__ == '__main__': 
    create()
