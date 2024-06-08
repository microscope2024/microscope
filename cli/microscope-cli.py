import argparse
import os
import sys

from rebuild.lib import rebuild_lib, open_lib

sys.path.append(os.path.join(sys.path[0], ".."))
from microscope_schema.schema import *
from query.run import *
from extractor.extractor import Extractor
from database.create import database_create

MICROSCOPE_HOME = os.path.abspath(os.path.join(os.path.join(sys.path[0], "..")))


def extractor_choices():
    extractor_list = list()
    for name, value in vars(Extractor).items():
        if "extractor" in name:
            extractor_list.append(name.split("_")[0])
    return extractor_list


def parse_args():
    global MICROSCOPE_HOME
    parser = argparse.ArgumentParser(description='microscope-cli',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--version", "-v", dest='version', action="store_true", help='version')
    parser.add_argument("--microscope-home", "-microscope-home", dest='microscope_home',
                        help='microscope home, You can specify the microscope location yourself')
    parser.add_argument('--microscope-cli-internal', dest='microscope_home_internal', help=argparse.SUPPRESS)
    parser.add_argument('--verbose', action='store_true', help='Enable verbose mode')
    subparsers = parser.add_subparsers(title='subcommands', dest='subcommand')
    subparser_query = subparsers.add_parser('query', help='execute datalog script')
    sub_subparser_query = subparser_query.add_subparsers(title='query_subcommands', dest='query_subcommands')
    subparser_query_run = sub_subparser_query.add_parser('run', help='execute datalog script')
    subparser_query_run.add_argument("--database", '-d', help='Directory to a datalog database to query')
    subparser_query_run.add_argument("--format", '-f', choices=['csv', 'json'], default='json',
                                     help='Select output format. default output json')
    subparser_query_run.add_argument("--output", '-o', default=os.getcwd(),
                                     help='Select output dir, The output file will have the same name as the Godel '
                                          'script, but with the {.json} extension')
    subparser_query_run.add_argument("--timeout", '-t', type=int, default=3600,
                                     help='Set query timeout in seconds, default 3600')
    subparser_query_run.add_argument("--gdl", '-gdl', required=True, nargs="*", dest="datalog_dir",
                                     help='The location of the datalog script that needs to execute')
    subparser_query_run.add_argument('--verbose', action='store_true', help='Enable verbose mode')

    subparser_database = subparsers.add_parser('database', help='data extract')
    sub_subparser_database = subparser_database.add_subparsers(title='database_subcommands',
                                                               dest='database_subcommands')
    subparser_database_create = sub_subparser_database.add_parser('create', help='data extract')
    subparser_database_create.add_argument("--source-root", '-s', required=True,
                                           help='Select source root,default to current directory')
    subparser_database_create.add_argument('--data-language-type', '-lang', nargs="*", dest="language",
                                           choices=extractor_choices(), required=True, help='data language type, Pass '
                                                                                            'in parameters separated '
                                                                                            'by whitespace. e.g. '
                                                                                            '-lang java xml')
    subparser_database_create.add_argument("--output", '-o', required=True, help='Database generation directory')
    subparser_database_create.add_argument("--timeout", '-t', type=int, default=3600,
                                           help='Set extract timeout in seconds, default 3600')
    subparser_database_create.add_argument('--verbose', action='store_true', help='Enable verbose mode')
    subparser_database_create.add_argument('--overwrite', action='store_true',
                                           help='whether to overwrite the database, Default not')
    subparser_database_create.add_argument('--extraction-config-file',
                                           help='Extractor execute option file, The requirement is a json file')
    subparser_database_create.add_argument('--extraction-config', nargs="*", help='Extractor execute option,'
                                                                                  'java.a=b will regard as "java" : {'
                                                                                  '"a" : "b"} in '
                                                                                  'extraction-config-file，Parameters '
                                                                                  'other than a.b=c will not be '
                                                                                  'accepted')
    subparser_rebuild = subparsers.add_parser('rebuild', help='rebuild tool')    
    sub_subparser_rebuild = subparser_rebuild.add_subparsers(title='rebuild_subcommands', dest='rebuild_subcommands')
    subparser_rebuild_lib = sub_subparser_rebuild.add_parser('lib', help='rebuild lib')
    subparser_rebuild_lib.add_argument('--data-language-type', '-lang', nargs="*", dest="language",
                                       choices=open_lib() + ["all"], required=True, help='data language type, Pass '
                                                                                         'in parameters separated '
                                                                                         'by whitespace. e.g. '
                                                                                         '-lang java xml')
    subparser_rebuild_lib.add_argument('--verbose', action='store_true', help='Enable verbose mode')
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        logging.warning("please give conf to start microscope as help, it will not start")
        return

    if args.microscope_home_internal:
        MICROSCOPE_HOME = args.microscope_home_internal
    if args.microscope_home:
        MICROSCOPE_HOME = args.microscope_home
    microscope(MICROSCOPE_HOME)

    Extractor()
    if args.version:
        print(microscope.version)
        return
    if args.verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level=log_level)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

    console_handler.setFormatter(formatter)
    logging.basicConfig(level=log_level, handlers=[console_handler])

    logging.info("microscope %s will start", microscope.version)
    if args.subcommand == "query":
        if args.query_subcommands == "run":
            query_run(args)
    elif args.subcommand == "database":
        if args.database_subcommands == "create":
            database_create(args)
    elif args.subcommand == "rebuild":
        if args.rebuild_subcommands == "lib":
            rebuild_lib(args)
    else:
        logging.warning("please give conf to start microscope, it will not start")
    return


if __name__ == '__main__':
    parse_args()
