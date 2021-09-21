import subprocess
key = 'tag'
image_tag = 456
path = './a.yaml'

subprocess.check_call(
            f'sed -i "s/{key}:.*/{key}: \\\"{image_tag}\\\"/g" {path}', shell=True)
