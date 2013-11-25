from setuptools import setup

readme = open('readme.md').read()
setup(name='PyRx',
      version='0.02',
      #author='Philip Schleihauf',
      #author_email='uniphil@gmail.com',
      license='GPLv2',
      description='Rx schema and validation system',
      long_description=readme,
      url='https://github.com/uniphil/pyrx',
      py_modules=['pyrx'])
