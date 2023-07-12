import os

from dotenv import load_dotenv

load_dotenv(verbose=True, override=True)

WORKING_DIR = "/app/workspace"
GITOPS_REPO = os.getenv("GITOPS_REPO")
GITOPS_BRANCH = os.getenv("GITOPS_BRANCH")
GITOPS_KEYPATH = os.getenv("GITOPS_KEYPATH", "/root/.ssh/id_rsa")
GITOPS_USERNAME = os.getenv("GITOPS_USERNAME")
GITOPS_USERMAIL = os.getenv("GITOPS_USERMAIL")
SECRET = os.getenv("SECRET")
