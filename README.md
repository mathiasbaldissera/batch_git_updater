# batch_git_updater
A simple python script to update the develop branch of all folders in current folder

Just run `python3 updater.py` and see the magic. You can specify manualy the folders inside the script or use one of the args below

Possible args:

    --help                show help
    --all-folders         run the script on all folders in current directory
    --ignore              folders to ignore when running the script
    --only                use only specified folders
    --update-branch       name of the branch to update. Default: develop
    --current             update only current branch. The script will not change to develop (or specified)
    --stay-develop        will not checkout back to previous branch

