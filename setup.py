from setuptools import setup

setup(name='schemadisplay-magic',
      packages=['schemadisplay_magic'],
      install_requires=['ipython-sql', 'sqlalchemy_schemadisplay', 'graphviz'],
      dependency_links=['git+https://github.com/fschulze/sqlalchemy_schemadisplay.git']
)