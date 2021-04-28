import yaml
import requests
import zipfile
from datetime import datetime
import os


def get_time_filename():
    return datetime.today().strftime('%Y-%m-%d_%H%M%S') + ".zip"


def upload(filename, url, key):
    with open(filename, 'rb') as f:
        r = requests.post(url,
                          files={'file': f},
                          headers={'Authorization': key})
        print(r.json())


def deploy(build_path, arch_name, url, key):
    zip(build_path, arch_name)
    upload(arch_name, url, key)
    os.remove(arch_name)


def main():
    config_file_path = "config.yaml"
    config = yaml.load(open(config_file_path, encoding="utf-8",
                            mode="r"), Loader=yaml.SafeLoader)    
    archive_name = "./" + get_time_filename()

    build_path = config["build_path"]
    url = config["deploy_url"]
    key = config["deploy_key"]

    deploy(build_path, archive_name, url, key)

def zip(path, archname):
    archive = zipfile.ZipFile(archname, "w", zipfile.ZIP_DEFLATED)
    if os.path.isdir(path):
        _zippy(path, path, archive)
    else:
        _, name = os.path.split(path)
        archive.write(path, name)
    archive.close()
    
def _zippy(base_path, path, archive):
    paths = os.listdir(path)
    for p in paths:
        p = os.path.join(path, p)
        if os.path.isdir(p):
            _zippy(base_path, p, archive)
        else:
            archive.write(p, os.path.relpath(p, base_path))

if __name__ == "__main__":
    main()
