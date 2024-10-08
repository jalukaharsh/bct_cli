"""Main module for Command Line Interface (CLI) for Bare Cove Technology (BCT)"""

from PyInquirer import prompt, print_json
import json 
import argparse
import bct_create, bct_base64
import os 
import re


def run_bct_cli(): 
    parser = argparse.ArgumentParser(description='BCT CLI Interface')
    parser.add_argument('functionality', choices=['create', 'base64'], 
                        help=' create: Create a project from template \n base64: Encode private key to base64')

    if not os.path.exists('config.json'):
        create_config()

    config_status = validate_config()
    
    if config_status:
        args = parser.parse_args()

        if args.functionality == 'create': 
            bct_create.create()
        elif args.functionality == 'base64': 
            bct_base64.base64_encoder()


def create_config(): 
    config_json_content = {
        "localUrlJson": True, 
        "templateUrlApi": "https://bct-cli-bucket.s3.ap-southeast-1.amazonaws.com/template.json",
        "templateUrlPath": "/Users/jameshu/CompanyProjects/bct-cli/template.json"
    }

    with open('config.json', 'w') as f: 
        json.dump(config_json_content, f)


def validate_config(): 
    with open('config.json', 'r') as f: 
        config_content = json.load(f) 
    status = True

    if config_content["localUrlJson"] is False:
        url_regex = r'/^http[s]?:\/\/.*/'
        url = re.compile(url_regex)
        template_url_api = config_content["templateUrlApi"]
        if url.match(template_url_api): 
            print('Config file is valid')
        else: 
            print('Online config file is invalid, please check templateUrlApi')
            status = False
    else: 
        local_url_json = config_content["templateUrlPath"]
        if os.path.exists(local_url_json): 
            print('Config file is valid')
        else: 
            print('Local config file is invalid, please check templateUrlPath')
            status = False
    return status

if __name__ == '__main__': 
    run_bct_cli()