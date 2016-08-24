import subprocess
import smtplib
from email.mime.text import MIMEText
#import settings
try:
    from settings import SMTP
except:
    pass

notify = False
smtp_settings = {}
if 'settings' in locals():
    if hasattr(settings, 'SMTP'):
        notify = True
        smtp_settings = settings.SMTP
else:
    if 'SMTP' in locals():
        notify = True
        smtp_settings = SMTP


def notify(subject, message, server: dict=smtp_settings):
    srv = server.get('server', 'localhost')
    port = server.get('port', 25)
    user = server.get('user')
    pwd = server.get('password', '')
    fromaddr = server.get('fromaddr')
    toaddrs = server.get('toaddrs', [])
    smtp_srv = smtplib.SMTP(srv, port)
    if user:
        smtp_srv.login(user, pwd)
    msg = MIMEText(message)
    msg['Subject'] = subject
    smtp_srv.send_message(msg, fromaddr, toaddrs)
    smtp_srv.quit()


def run_shell_command(command, notification_body=None):

    msg = notification_body
    print('Running:')
    print(command)
    msg += '\nRunning:\n{}'.format(command)
    command_parsed = command.split()
    res = subprocess.run(command_parsed, universal_newlines=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    if res.returncode !=0:
        msg += 'Error: {}\n'.format(str(res.stderr))
        print('Error: ' + str(res.stderr))
    else:
        msg += '{}\n'.format(res.stdout)
        print(str(res.stdout))
    return msg

if __name__ == '__main__':
    run_shell_command('/sbin/ifconfig', notify)