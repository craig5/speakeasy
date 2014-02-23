from distutils.core import setup
import distutils.command
try:
    import virtualenv
    _VE_LOADED = True
except ImportError as e:
    _VE_LOADED = False
import os
import sys
import subprocess


_PACKAGE_NAME           = 'speakeasy'
_HOME_DIR               = os.path.expanduser('~')
_DEFAULT_VE_BASE_DIR    = os.path.join(_HOME_DIR, '.virtualenvs')

# errors
_ERROR_NO_VE_LIB  = 11
_ERROR_VE_EXISTS  = 12


class Activate(distutils.cmd.Command):
    """Activate virtualenv."""
    description = "Activate virtualenv."
    user_options = []

    def run(self):
        ve_dir = os.path.join(self.ve_base_dir, _PACKAGE_NAME)
        activate_script = os.path.join(ve_dir, 'bin', 'activate')
        print "Run: source {0}".format(activate_script)

    def finalize_options(self):
        pass

    def initialize_options(self):
        pass

    def __init__(self, dist):
        self.finalized = None
        self.dist = dist
        self.ve_base_dir = os.environ.get('VIRTUALENV_DIR',
                _DEFAULT_VE_BASE_DIR)


class VirtualEnv(distutils.cmd.Command):
    """Install virtualenv."""
    description = "Manage virtualenv."
    user_options = []

    def run(self):
        #print dir(self)
        #print dir(self.dist)
        if not _VE_LOADED:
            self.warn("Cannot load virtualenv lib.")
            sys.exit(_ERROR_NO_VE_LIB)
        ve_dir = os.path.join(self.ve_base_dir, _PACKAGE_NAME)
        if os.path.exists(ve_dir):
            self.warn("Dir exists: {0}".format(ve_dir))
            #sys.exit(_ERROR_VE_EXISTS)
        else:
            self.warn("Creating virtualenv dir: {0}".format(ve_dir))
        #self.debug_print("Virtualenv dir: {0}".format(ve_dir))
        virtualenv.create_environment(ve_dir, site_packages=False)
        bin_dir = os.path.join(ve_dir, 'bin')
        print bin_dir
        virtualenv.install_activate(ve_dir, bin_dir)
        proc = subprocess.Popen(['which','pip'],
                stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        (stdout,stderr) = proc.communicate()
        print 'stdout:',stdout
        print 'stderr:',stderr

        pip = os.path.join(bin_dir, 'pip')
        python = os.path.join(bin_dir, 'python')

        install_reqs = [pip, 'install', '-r', 'requirements.txt']
        proc = subprocess.Popen(install_reqs,
                stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        (stdout,stderr) = proc.communicate()
        print 'stdout:',stdout
        print 'stderr:',stderr

        install_pkg = [python, 'setup.py', 'install']
        proc = subprocess.Popen(install_pkg,
                stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        (stdout,stderr) = proc.communicate()
        print 'stdout:',stdout
        print 'stderr:',stderr


    def finalize_options(self):
        pass

    def initialize_options(self):
        pass

    def __init__(self, dist):
        self.finalized = None
        self.dist = dist
        self.ve_base_dir = os.environ.get('VIRTUALENV_DIR',
                _DEFAULT_VE_BASE_DIR)


setup(
    name        = _PACKAGE_NAME,
    version     = '1.0.1',
    description = 'Metrics aggregation server',
    author      = 'Eric Wong',
    packages    = ['speakeasy', 'speakeasy.emitter'],
    scripts     = ['bin/speakeasy'],
    cmdclass    = {'virtualenv':VirtualEnv, 'activate':Activate},
    )
