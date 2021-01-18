import os
import shlex
import sys
from subprocess import check_call as call, check_output

folders = [
    'manual insert folders here'
]
failed = []
with_changes = []
update_branch = 'develop'
current = False


def _sh(string):
    return shlex.split(string)


if '--help' in sys.argv:
    print('--help                this')
    print('--all-folders         run the script on all folders in current directory')
    print('--ignore              folders to ignore when running the script')
    print('--only                use only specified folders')
    print('--update-branch       name of the branch to update. Default: develop')
    print('--current             update only current branch. The script will not change to develop (or specified)')
    exit(0)

if '--all-folders' in sys.argv:
    folders = [x for x in next(os.walk('.'))[1]]
    folders = sorted(folders)

if '--ignore' in sys.argv:
    ignore_index = sys.argv.index('--ignore')
    ignore_list = sys.argv[ignore_index + 1].split(',')
    print(ignore_list)
    folders = [x for x in folders if x not in ignore_list]

if '--only' in sys.argv:
    index = sys.argv.index('--only')
    folders = sys.argv[index + 1].split(',')

if '--update-branch' in sys.argv:
    index = sys.argv.index('--update-branch')
    update_branch = sys.argv[index + 1]

if '--current' in sys.argv:
    current = True


def update(path):
    try:
        print(f'======== updating {path.upper()}===========')
        current_branch = str(check_output(_sh(f'git -C {path} rev-parse --abbrev-ref HEAD'))) \
            .replace('b\'', '').replace('\\n\'', '')
        print(current_branch)
        has_stash = 'Saved working directory and index' in str(check_output(_sh(f'git -C {path} stash')))
        if not current and current_branch != update_branch:
            call(_sh(f'git -C {path} checkout {update_branch}'))

        call(_sh(f'git -C {path} pull'))

        if not current and current_branch != update_branch:
            call(_sh(f'git -C {path} checkout {current_branch}'))
        if has_stash:
            with_changes.append(path)
            call(_sh(f'git -C {path} stash pop'))
    except:
        failed.append(path)
    print(f'\n\n')


for path in folders:
    update(path)

if len(failed) > 0:
    print('xxxxxxxxxxxxxxxxxxxxxxxxx')
    print('FAILED TO UPDATE DEVELOP:')
    print(failed)
if len(with_changes) > 0:
    print('===================')
    print('Repos with changes:')
    print(with_changes)
