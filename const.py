import os
from dotenv import load_dotenv
load_dotenv(verbose=True, override=True)

WORKING_DIR = '/app/workspace'
GITOPS_REPO = os.getenv('GITOPS_REPO')
GITOPS_KEYPATH = os.getenv('GITOPS_KEYPATH')
GITOPS_USERNAME = os.getenv('GITOPS_USERNAME')
GITOPS_USERMAIL = os.getenv('GITOPS_USERMAIL')
SECRET = os.getenv('SECRET')
