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
        }
    ]   

    answers = prompt(questions)
    template = answers['template']
    project_name = answers['projectName']
    bitbucket_url = answers['bitbucketProjectUrl']

    template_url = template_dict[template]
    clone_template_call = 'git clone ' + template_url + ' ' + project_name + ' --depth=1'

    subprocess.run(clone_template_call, shell=True)

    delete_git_dir(project_name)

    if bitbucket_url == '': 
        print('Cloning successful!')
    else: 
        git_init = 'git init ' + project_name
        git_remote_add_origin = 'git remote add origin ' + project_name + ' ' + bitbucket_url
        git_fetch = 'git fetch --all '
        git_reset = 'git reset --hard origin/HEAD ' + project_name

        subprocess.run(git_init)
        subprocess.run(git_remote_add_origin)
        subprocess.run(git_fetch)
        subprocess.run(git_reset)


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
