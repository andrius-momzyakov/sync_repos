from settings import REPOS
from utils import run_shell_command, notify
import os

msg_subj = "Repositories' refreshment"
msg_body = ""
for rep_path in REPOS:
    spl_path = rep_path.rsplit('/', 1) 
    print('===> Updating {}: '.format(spl_path[len(spl_path)-1]))
    msg_body += '\n===> Updating {}: '.format(spl_path[len(spl_path)-1])
    print('Making cd {}...'.format(rep_path))
    msg_body += '\nMaking cd {}...'.format(rep_path)
    os.chdir(rep_path)
    msg_body = run_shell_command('git config credential.helper store', notification_body=msg_body)
    msg_body = run_shell_command('git pull --all', notification_body=msg_body)

if notify:
    notify(subject=msg_subj, message=msg_body)