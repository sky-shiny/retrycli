#!/usr/bin/env python
import logging
import subprocess
from retrying import retry
logging.basicConfig()
LOG = logging.getLogger('retrycli')
LOG.setLevel(logging.ERROR)


class ShellCmdError(Exception):
    """Ipmi command failure exception."""
    def __init__(self, message, stderr=None, returncode=-1):
        self.returncode = returncode
        self.stderr = stderr
        Exception.__init__(self, message)

def retry_if_ShellCmdError(exception):
    """Return True if we should retry (in this case when it's an ShellCmdError), False otherwise"""
    return isinstance(exception, ShellCmdError)


@retry(wait_exponential_multiplier=500, wait_exponential_max=10000, stop_max_attempt_number=7, retry_on_exception=retry_if_ShellCmdError)
def shell_command(**kwargs):
    """
    Wrap the shell command args in the retry decorator
    """
    print('(re)trying: ' + ' '.join(kwargs['shell_argument']))
    try:
        LOG.debug(kwargs['shell_argument'])
        proc = subprocess.Popen(kwargs['shell_argument'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        with proc.stdout:
            for line in iter(proc.stdout.readline, b''):
                print(line)
        with proc.stderr:
            for line in iter(proc.stderr.readline, b''):
                LOG.error(line)
        proc.wait()
        if proc.returncode > 0:
            raise ShellCmdError("Error executing: '{0}'.".format(kwargs['shell_argument']), stderr=proc.stderr, returncode=proc.returncode)
        else:
            return
    except KeyboardInterrupt:
        proc.send_signal(signal.SIGINT)
