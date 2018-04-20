"""schemadisplay magic"""
__version__ = '0.0.1'

from .schemadisplay import SchemaDisplayMagic


def load_ipython_extension(ipython):
    ipython.register_magics(SchemaDisplayMagic)