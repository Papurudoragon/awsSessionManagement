# AWS CLI Session Script

## Overview
This script allows you to manage AWS profile sessions by creating new profiles and selecting existing ones. It interacts with your AWS credentials and config files to add new profiles and select existing ones for use with the AWS CLI or SDK.

## Requirements
Before using the script, make sure to install the required dependencies by running the following command:
```sh
python3 -m pip install -r requirements.txt
```

## Usage
1. Run the script by executing:
```python3 awsconnect.py```

## Notes
- The script automatically interacts with your AWS credentials and config files located in ~/.aws/ directory.
- After running the script, the selected AWS profile becomes the active session for the current terminal session.
- Make sure to have the AWS CLI installed and configured with at least one profile before running the script.
- If you're using IAM roles with your AWS profiles, the selected profile will be used as the assumed role during your terminal session.

## Author
Papv2