"""Utilities to call shell programs."""

import os
import logging
import platform

if platform.system() == 'Windows':
    import pbs as sh
else:
    import sh

from . import common
from .exceptions import ShellError

CMD_PREFIX = "$ "
OUT_PREFIX = "> "

log = logging.getLogger(__name__)


def call(name, *args, _show=True, _capture=False, _ignore=False):
    """Call a shell program with arguments."""
    msg = CMD_PREFIX + ' '.join([name] + list(args))
    if _show:
        common.show(msg)
    else:
        log.debug(msg)

    if name == 'cd' and len(args) == 1:
        return os.chdir(args[0])

    try:
        program = sh.Command(name)
        if _capture:
            line = program(*args).strip()
            log.debug(OUT_PREFIX + line)
            return line
        else:
            line = program(*args)
            log.debug(OUT_PREFIX + line.strip())
    except sh.ErrorReturnCode as exc:
        msg = "\n  IN: '{}'{}".format(os.getcwd(), exc)
        if _ignore:
            log.debug("Ignored error from call to '%s'", name)
        else:
            raise ShellError(msg)


def mkdir(path):
    call('mkdir', '-p', path)


def cd(path, _show=True):
    call('cd', path, _show=_show)


def ln(source, target):
    dirpath = os.path.dirname(target)
    if not os.path.isdir(dirpath):
        mkdir(dirpath)
    call('ln', '-s', source, target)


def rm(path):
    call('rm', '-rf', path)
