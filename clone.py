import os 

def clone_from_url(git_repo_url):
    clone = "git clone -q --recurse-submodules --depth 1 " + git_repo_url  
    os.system(clone)
    return "Cloned!"