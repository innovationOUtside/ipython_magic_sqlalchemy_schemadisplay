from IPython.core.magic import (
    magics_class, line_magic, line_cell_magic, Magics)
from IPython.core.display import Image, HTML, SVG


from argparse import ArgumentParser
import shlex
import configparser
import os

from csv import reader
from sqlalchemy import MetaData
from sqlalchemy_schemadisplay import create_schema_graph
from graphviz import Source

@magics_class
class SchemaDisplayMagic(Magics):
    def __init__(self, shell, cache_display_data=False):
        super(SchemaDisplayMagic, self).__init__(shell)
        self.cache_display_data = cache_display_data

    @line_cell_magic
    def schema(self,line, cell=''):
        '''Format.'''
        
        parser = ArgumentParser()
        parser.add_argument('-D', '--database_config', default=None)
        parser.add_argument('-c', '--connection_string', default=None)
        parser.add_argument('-t', '--include_tables', default=None)
        parser.add_argument('-k', '--show_column_keys', action='store_false')
        parser.add_argument('-d', '--show_datatypes', action='store_false')
        
        args = parser.parse_args(shlex.split(line))
        
        if args.connection_string is None and args.database_config is None:
            return
        
        include_tables = [i for i in reader([args.include_tables])][0] if args.include_tables is not None else None
        
        if args.connection_string is not None:
            connection_string = args.connection_string
        else:
            # Create a connection string from settings
            config = configparser.ConfigParser()
            if not "HOME" in os.environ:
                print("Can't find $HOME environment variable.")
                return
            config.read(f'{os.environ["HOME"]}/.jupysql/connections.ini')
            if not config.sections() or args.database_config not in config.sections():
                print(f"Error: can't find {args.database_config} in ~/.jupysql/connections.ini")
                return
            else:
                connection_string = "{drivername}://{username}:{password}@{host}:{port}/{database}".format(**config[args.database_config])
                #print(f"Using connection string: {connection_string}")
        graph = create_schema_graph(connection_string=connection_string,
            show_datatypes=args.show_datatypes, # The image would get nasty big if we'd show the datatypes
            show_indexes=False, # ditto for indexes
            rankdir='LR', # From left to right (instead of top to bottom),
            restrict_tables=include_tables,
            concentrate=False, # Don't try to join the relation lines together
            show_column_keys=args.show_column_keys)

        return Source(graph.create_dot().decode("utf-8") )

def load_ipython_extension(ipython):
    ipython.register_magics(SchemaDisplayMagic)
    
ip = get_ipython()
ip.register_magics(SchemaDisplayMagic)