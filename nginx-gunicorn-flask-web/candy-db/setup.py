#!/usr/bin/env python
"""Setup for the candydb module of CandyBudget.
"""
import subprocess
from setuptools import setup, find_packages
import os

def make_version():
    """Generates a version number using `git describe`.

    Returns:
      version number of the form "3.1.1.dev127+g413ed61".
    """
    def _minimal_ext_cmd(cmd):
        """Run a command in a subprocess.

        Args:
          cmd: list of the command

        Returns:
          output from the command
        """
        # construct minimal environment
        env = {}
        for k in ['SYSTEMROOT', 'PATH']:
            value = os.environ.get(k)
            if value is not None:
                env[k] = value
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = subprocess.Popen(cmd,
                               stdout=subprocess.PIPE,
                               env=env).communicate()[0]
        return out

    version = 'unknown'

    if os.path.exists('../.git'):
        try:
            out = _minimal_ext_cmd(['git',
                                    'describe',
                                    '--tags',
                                    '--match',
                                    'v*'])
            out = out.decode("utf-8")
            version = out.strip().split("-")
            if len(version) > 1:
                version, dev, sha = version
                version = "%s.dev%s+%s" % (version[1:], dev, sha)
            else:
                version = version[0][1:]
        except OSError:
            import warnings
            warnings.warn("Could not run ``git describe``")
    elif os.path.exists('models.egg-info'):
        from models import get_version
        version = get_version()
    return version

setup(name='candydb',
      version='0.1',
      description='Package for CandyBudget Database Models',
      packages=find_packages(),
      package_data={'' : ['test/*.py']})