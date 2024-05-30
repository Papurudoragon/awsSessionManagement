import boto3
from botocore.exceptions import ProfileNotFound
import os
import configparser
import time
import subprocess
import sys

# global vars
aws_credentials_path = os.path.expanduser("~/.aws/credentials")
aws_config_path = os.path.expanduser("~/.aws/config")
profiles = set()

# check if aws cli exists, if not prompt user to install it
def awscli_check():
    res = subprocess.run(['aws', '--version'], capture_output=True, text=True)
    if res.returncode != 0 or not res.stdout:
        print("\nAWS CLI is either not installed or found in PATH, please install or add to PATH To continue.")
        sys.exit(1)
    else:
        return

# create AWS profile if not exists
def create_awsprofile(name):
    global aws_credentials_path, aws_config_path, accounts
    print("\n\naccount creation process. \n\n")

    print(f"profile name: {name}")
    access_key = input('enter aws access key: ').upper()
    secret_access_key = input('enter aws secret access key: ').upper()
    region = input('enter aws region [default: us-east-1]: ').lower()
    if region == '':
        region = 'us-east-1'

    # make cred file if not exists
    os.makedirs(os.path.dirname(aws_credentials_path), exist_ok=True)
    if not os.path.exists(aws_credentials_path):
        with open(aws_credentials_path, 'w') as f:
            f.write('')

    # make AWS config file if not exists
    os.makedirs(os.path.dirname(aws_config_path), exist_ok=True)
    if not os.path.exists(aws_config_path):
        with open(aws_config_path, 'w') as f:
            f.write('')

    # Append credentials to the credentials file
    with open(aws_credentials_path, 'a') as credentials_file:
        credentials_file.write(f'\n[{name}]\n')
        credentials_file.write(f'aws_access_key_id = {access_key}\n')
        credentials_file.write(f'aws_secret_access_key = {secret_access_key}\n')

    # Append configuration to the config file
    with open(aws_config_path, 'a') as config_file:
        config_file.write(f'\n[profile {name}]\n')
        config_file.write(f'region = {region}\n')

    print(f"Profile '{name}' created successfully.\n")
    choice = input('Do you want to log into this profile? (y/n --invalid option is also treated as n)').lower()
    if choice == 'y':
        aws_signin(name)
    elif choice == 'n':
        time.sleep(1)
        return "option 'n' selected. exiting..."
    else:
        time.sleep(1)
        return "invalid option selected (this will be treated as n). exiting..."
    
    return

# list aws profiles
def get_aws_profiles():
    global aws_credentials_path, aws_config_path, profiles

    # return false if path not exists
    if not os.path.exists(aws_credentials_path):
        print(f"The AWS credentials file does not exist at {aws_credentials_path}.")
        return False
    
    config = configparser.ConfigParser()
    config.read(aws_credentials_path)

    # list avail profile names
    profile_list = config.sections()
    print("profiles found: \n")
    for profile in profile_list:
        profiles.add(profile)
        print(profile)
    
    return profiles

def get_selected_profile():
    profiles = get_aws_profiles()
    profile = input("\nenter a profile name to use, or enter a new profile name to create one: ").lower()
    if profile not in profiles:
        create_awsprofile(profile)
    else:
        aws_signin(profile)
    
    return

# function to create aws session
def create_session_aws(profile_name):
    try:
        return boto3.Session(profile_name=profile_name)
    except ProfileNotFound as e:
        return f"Error creatin aws session: {e}"

# now we need to sign in with the selected profile
def aws_signin(profile):

    session = create_session_aws(profile)
    if session == False:
        return f"\naws session not created.\n"
    else: 
        print(f"\nsession created successfully: {session}\n")
        print("run 'aws sts get-caller-identity' to view details on the session.\n")
    return

def main():
    awscli_check()
    get_selected_profile()

if __name__=="__main__":
    main()