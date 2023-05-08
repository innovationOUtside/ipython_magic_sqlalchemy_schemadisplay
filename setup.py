from setuptools import setup

from os import path

def get_long_description():
    with open(
        path.join(path.dirname(path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()
   

def get_requirements(fn='requirements.txt', nogit=True):
   """Get requirements."""
   if path.exists(fn):
      with open(fn, 'r') as f:
        requirements = [r.split()[0].strip() for r in f.read().splitlines() if r and not r.startswith('#')]
   else:
     requirements = []

   if nogit:
       requirements = [r for r in requirements if not 'git+' in r]
   return requirements
   
requirements = get_requirements()

print(f'Requirements: {requirements}')

setup(author='Tony Hirst',
    author_email='tony.hirst@open.ac.uk',
    description='Python package installation for ipython_magic_sqlalchemy_schemadisplay',
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    license='MIT',
    url='https://github.com/innovationOUtside/ipython_magic_sqlalchemy_schemadisplay',
    version='0.0.6',
    name='schemadisplay-magic',
    packages=['schemadisplay_magic', 'sqlalchemy_schemadisplay'],
    install_requires=requirements
)
