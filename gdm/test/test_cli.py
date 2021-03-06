# pylint: disable=no-self-use

from unittest.mock import Mock, patch
import logging

import pytest

from gdm import cli
from gdm.common import _Config


class TestMain:

    """Unit tests for the top-level arguments."""

    def test_main(self):
        """Verify the top-level command can be run."""
        mock_function = Mock(return_value=True)

        cli.main([], mock_function)

        mock_function.assert_called_once_with(root=None)

    def test_main_fail(self):
        """Verify error in commands are detected."""
        with pytest.raises(SystemExit):
            cli.main([], Mock(return_value=False))

    def test_main_help(self):
        """Verify the help text can be displayed."""
        with pytest.raises(SystemExit):
            cli.main(['--help'])

    def test_main_none(self):
        """Verify it's an error to specify no command."""
        with pytest.raises(SystemExit):
            cli.main([])

    def test_main_interrupt(self):
        """Verify a command can be interrupted."""
        with pytest.raises(SystemExit):
            cli.main([], Mock(side_effect=KeyboardInterrupt))

    def test_main_error(self):
        """Verify runtime errors are handled."""
        with pytest.raises(SystemExit):
            cli.main([], Mock(side_effect=RuntimeError))


class TestInstall:

    """Unit tests for the `install` command."""

    @patch('gdm.commands.install')
    def test_install(self, mock_install):
        """Verify the 'install' command can be run."""
        cli.main(['install'])

        mock_install.assert_called_once_with(
            root=None, depth=None, force=False, fetch=False, clean=False)

    @patch('gdm.commands.install')
    def test_install_root(self, mock_install):
        """Verify the project's root can be specified."""
        cli.main(['install', '--root', 'mock/path/to/root'])

        mock_install.assert_called_once_with(
            root='mock/path/to/root', depth=None,
            force=False, fetch=False, clean=False)

    @patch('gdm.commands.install')
    def test_install_force(self, mock_install):
        """Verify dependencies can be force-installed."""
        cli.main(['install', '--force'])

        mock_install.assert_called_once_with(
            root=None, depth=None, force=True, fetch=False, clean=False)

    @patch('gdm.commands.install')
    def test_install_fetch(self, mock_install):
        """Verify fetching can be enabled."""
        cli.main(['install', '--fetch'])

        mock_install.assert_called_once_with(
            root=None, depth=None, force=False, fetch=True, clean=False)

    @patch('gdm.commands.install')
    def test_install_clean(self, mock_install):
        """Verify dependency cleaning can be enabled."""
        cli.main(['install', '--clean'])

        mock_install.assert_called_once_with(
            root=None, depth=None, force=False, fetch=False, clean=True)

    @patch('gdm.commands.install')
    def test_install_specific_sources(self, mock_install):
        """Verify individual dependencies can be installed."""
        cli.main(['install', 'foo', 'bar'])

        mock_install.assert_called_once_with(
            'foo', 'bar', root=None, depth=None,
            force=False, fetch=False, clean=False)

    @patch('gdm.commands.install')
    def test_install_with_depth(self, mock_update):
        """Verify the 'install' command can be limited by depth."""
        cli.main(['install', '--depth', '5'])

        mock_update.assert_called_once_with(
            root=None, depth=5, force=False, fetch=False, clean=False)

    @patch('gdm.commands.install', Mock())
    def test_install_with_depth_invalid(self):
        """Verify depths below 1 are rejected."""
        with pytest.raises(SystemExit):
            cli.main(['install', '--depth', '0'])
        with pytest.raises(SystemExit):
            cli.main(['install', '--depth', '-1'])


class TestUpdate:

    """Unit tests for the `update` command."""

    @patch('gdm.commands.update')
    def test_update(self, mock_update):
        """Verify the 'update' command can be run."""
        cli.main(['update'])

        mock_update.assert_called_once_with(
            root=None, depth=None,
            force=False, clean=False, recurse=False, lock=None)

    @patch('gdm.commands.update')
    def test_update_recursive(self, mock_update):
        """Verify the 'update' command can be run recursively."""
        cli.main(['update', '--all'])

        mock_update.assert_called_once_with(
            root=None, depth=None,
            force=False, clean=False, recurse=True, lock=None)

    @patch('gdm.commands.update')
    def test_update_no_lock(self, mock_update):
        """Verify the 'update' command can disable locking."""
        cli.main(['update', '--no-lock'])

        mock_update.assert_called_once_with(
            root=None, depth=None,
            force=False, clean=False, recurse=False, lock=False)

    @patch('gdm.commands.update')
    def test_update_lock(self, mock_update):
        """Verify the 'update' command can enable locking."""
        cli.main(['update', '--lock'])

        mock_update.assert_called_once_with(
            root=None, depth=None,
            force=False, clean=False, recurse=False, lock=True)

    def test_update_lock_conflict(self):
        """Verify the 'update' command cannot specify both locking options."""
        with pytest.raises(SystemExit):
            cli.main(['update', '--lock', '--no-lock'])

    @patch('gdm.commands.update')
    def test_update_specific_sources(self, mock_install):
        """Verify individual dependencies can be installed."""
        cli.main(['update', 'foo', 'bar'])

        mock_install.assert_called_once_with(
            'foo', 'bar', root=None, depth=None,
            force=False, clean=False, recurse=False, lock=None)

    @patch('gdm.commands.update')
    def test_update_with_depth(self, mock_update):
        """Verify the 'update' command can be limited by depth."""
        cli.main(['update', '--depth', '5'])

        mock_update.assert_called_once_with(
            root=None, depth=5,
            force=False, clean=False, recurse=False, lock=None)


class TestList:

    """Unit tests for the `list` command."""

    @patch('gdm.commands.display')
    def test_list(self, mock_display):
        """Verify the 'list' command can be run."""
        cli.main(['list'])

        mock_display.assert_called_once_with(
            root=None, depth=None, allow_dirty=True)

    @patch('gdm.commands.display')
    def test_list_root(self, mock_display):
        """Verify the project's root can be specified."""
        cli.main(['list', '--root', 'mock/path/to/root'])

        mock_display.assert_called_once_with(
            root='mock/path/to/root', depth=None, allow_dirty=True)

    @patch('gdm.commands.display')
    def test_list_no_dirty(self, mock_display):
        """Verify the 'list' command can be set to fail when dirty."""
        cli.main(['list', '--no-dirty'])

        mock_display.assert_called_once_with(
            root=None, depth=None, allow_dirty=False)

    @patch('gdm.commands.display')
    def test_update_with_depth(self, mock_update):
        """Verify the 'list' command can be limited by depth."""
        cli.main(['list', '--depth', '5'])

        mock_update.assert_called_once_with(
            root=None, depth=5, allow_dirty=True)


def describe_lock():
    # pylint: disable=unused-variable

    @patch('gdm.commands.lock')
    def with_no_arguments(lock):
        cli.main(['lock'])
        lock.assert_called_once_with(root=None)

    @patch('gdm.commands.lock')
    def with_dependencies(lock):
        cli.main(['lock', 'foo', 'bar'])
        lock.assert_called_once_with('foo', 'bar', root=None)


class TestUninstall:

    """Unit tests for the `uninstall` command."""

    @patch('gdm.commands.delete')
    def test_uninstall(self, mock_uninstall):
        """Verify the 'uninstall' command can be run."""
        cli.main(['uninstall'])

        mock_uninstall.assert_called_once_with(
            root=None, force=False)

    @patch('gdm.commands.delete')
    def test_uninstall_root(self, mock_uninstall):
        """Verify the project's root can be specified."""
        cli.main(['uninstall', '--root', 'mock/path/to/root'])

        mock_uninstall.assert_called_once_with(
            root='mock/path/to/root', force=False)

    @patch('gdm.commands.delete')
    def test_uninstall_force(self, mock_uninstall):
        """Verify the 'uninstall' command can be forced."""
        cli.main(['uninstall', '--force'])

        mock_uninstall.assert_called_once_with(
            root=None, force=True)


class TestLogging:

    """Unit tests for logging."""

    arg_verbosity = [
        ('', 0),
        ('-v', 1),
        ('-vv', 2),
        ('-vvv', 3),
        ('-vvvv', 4),
        ('-vvvvv', 4),
        ('-q', -1),
    ]

    @staticmethod
    def mock_function(*args, **kwargs):
        """Placeholder logic for logging tests."""
        logging.debug(args)
        logging.debug(kwargs)
        logging.warning("warning")
        logging.error("error")
        return True

    @pytest.mark.parametrize("arg,verbosity", arg_verbosity)
    def test_level(self, arg, verbosity):
        """Verify verbose level can be set."""
        cli.main([arg] if arg else [], self.mock_function)
        assert verbosity == _Config.verbosity
