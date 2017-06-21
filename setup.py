#!/usr/bin/env python

import re
import uuid
from setuptools import setup, find_packages
from pip.req import parse_requirements


VERSIONFILE = "lunchbot/__init__.py"
ver_file = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, ver_file, re.M)

if mo:
    version = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

install_reqs = parse_requirements('requirements.txt', session=uuid.uuid1())
reqs = [str(req.req) for req in install_reqs]

setup(name="lunchbot",
      version=version,
      description="Slackbot to randomly pick a lunch destination nearby",
      license="MIT",
      author="shatnerz",
      author_email='andrew.ahlers@gmail.com',
      url="https://github.com/Shatnerz/lunchbot",
      packages=find_packages(exclude=['tests']),
      install_requires=reqs,
      keywords="slack lunch lunchbot",
      classifiers=[
          'Development Status :: 4 - Beta',
          'Topic :: Software Development :: Libraries',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.5',
      ],
      zip_safe=True)
