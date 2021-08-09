import json
import os
import subprocess
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from logzero import logger

from const import GITOPS_KEYPATH, GITOPS_REPO, GITOPS_USERMAIL, GITOPS_USERNAME, SECRET, WORKING_DIR

app = FastAPI()


class Request(BaseModel):
    app: Optional[str]
    env: Optional[str]
    image_tag: Optional[str]
    secret: Optional[str]


subprocess.check_call(
    f'git config --global user.email {GITOPS_USERNAME}', shell=True)
subprocess.check_call(
    f'git config --global user.name {GITOPS_USERMAIL}', shell=True)
git_env = os.environ.copy()
git_env['GIT_SSH_COMMAND'] = 'ssh -i /root/.ssh/id_rsa -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no'


@app.post('/helm')
async def helm(request: Request):
    if request.secret != SECRET:
        raise HTTPException(status_code=503)

    try:
        gitops_env = request.env
        gitops_app = request.app
        gitops_image_tag = request.image_tag

        hook_config = json.load(open('config.json'))
        app_config = hook_config.get(gitops_env).get(gitops_app)

        gitops_path = app_config.get('path')
        gitops_branch = app_config.get('branch')
        gitops_image_key = app_config.get('image_key')

        config_file_path = WORKING_DIR + gitops_path
        commit_message = f'CI: {gitops_env}.{gitops_app} => {gitops_image_tag}'
    except:
        raise HTTPException(status_code=400, detail='Config not found')

    delete_workspace(dir=WORKING_DIR)
    git_clone(repo=GITOPS_REPO, branch=gitops_branch, dir=WORKING_DIR)
    yaml_replace(path=config_file_path, key=gitops_image_key,
                 image_tag=gitops_image_tag)
    git_commit_n_push(path=WORKING_DIR, message=commit_message)

    return {'status': 'ok'}


def delete_workspace(dir: str):
    try:
        subprocess.check_call(f'rm -rf {dir}', shell=True)
    except Exception as ex:
        logger.info(f'{dir} not found')


def git_clone(repo: str, branch: str, dir: str):
    try:
        subprocess.check_call(
            f"git clone --branch {branch} {repo} {dir}", shell=True, env=git_env)
    except Exception as ex:
        logger.exception(ex)
        raise HTTPException(status_code=500)


def yaml_replace(path: str, key: str, image_tag: str):
    try:
        subprocess.check_call(
            f'sed -i "s/{key}:.*/{key}: {image_tag}/g" {path}', shell=True)
    except Exception as ex:
        logger.exception(ex)
        raise HTTPException(status_code=500)


def git_commit_n_push(path, message: str):
    try:
        subprocess.check_call(
            f'git commit -a -m "{message}"', shell=True, cwd=path, env=git_env)
        subprocess.check_call('git push', shell=True, cwd=path, env=git_env)
    except Exception as ex:
        logger.exception(ex)
        raise HTTPException(status_code=500)
