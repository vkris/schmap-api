#!/usr/bin/env python
from setuptools import setup, find_packages
import os, re

PKG='schmap-api'
VERSIONFILE = os.path.join('schmap_api', '_version.py')
verstr = "unknown"
try:
    verstrline = open(VERSIONFILE, "rt").read()
except EnvironmentError:
    pass # Okay, there is no version file.
else:
    MVSRE = r"^manual_verstr *= *['\"]([^'\"]*)['\"]"
    mo = re.search(MVSRE, verstrline, re.M)
    if mo:
        mverstr = mo.group(1)
    else:
        print "unable to find version in %s" % (VERSIONFILE,)
        raise RuntimeError("if %s.py exists, it must be well-formed" % (VERSIONFILE,))
    AVSRE = r"^auto_build_num *= *['\"]([^'\"]*)['\"]"
    mo = re.search(AVSRE, verstrline, re.M)
    if mo:
        averstr = mo.group(1)
    else:
        averstr = ''
    verstr = '.'.join([mverstr, averstr])

setup(name=PKG,
      version=verstr,
      description="schmap client to access schmap api",
      author="Vivek Krishna",
      author_email="v@generalsentiment.com",
      url="http://github.com/vkris/schmap-api/",
      packages = ['schmap_api'],
      #install_requires = ['zc-zookeeper-static'],
      license = "GS License",
      keywords="schmap",
      zip_safe = True,
      test_suite="tests",
      tests_require=['coverage', 'mock'])

