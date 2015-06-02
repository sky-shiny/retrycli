#!/usr/bin/env python
import logging
import subprocess
from retrying import retry
logging.basicConfig()
LOG = logging.getLogger('retrycli')
LOG.setLevel(logging.DEBUG)


class ShellCmdError(Exception):
    """Ipmi command failure exception."""
    def __init__(self, message, stderr=None, returncode=-1):
        self.stderr = stderr
        self.returncode = returncode
        Exception.__init__(self, message)


@retry(wait_exponential_multiplier=500, wait_exponential_max=10000, stop_max_attempt_number=7)
def shell_command(**kwargs):
    """
    Wrap the shell command args in the retry decorator
    """
    LOG.debug(kwargs['shell_argument'])
    proc = subprocess.Popen(kwargs['shell_argument'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if proc.returncode > 0:
        LOG.error("stderr: {0}".format(stderr))
        raise ShellCmdError("Error executing: '{0}'.".format(kwargs['shell_argument']), stderr=stderr, returncode=proc.returncode)
    else:
        return stdout
