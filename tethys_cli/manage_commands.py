"""
********************************************************************************
* Name: manage_commands.py
* Author: Nathan Swain
* Created On: 2015
* Copyright: (c) Brigham Young University 2015
* License: BSD 2-Clause
********************************************************************************
"""

from tethys_cli.cli_helpers import get_manage_path, get_django_manage_commands, run_process

MANAGE_START = 'start'
MANAGE_COLLECTSTATIC = 'collectstatic'
MANAGE_COLLECTWORKSPACES = 'collectworkspaces'
MANAGE_COLLECT = 'collectall'
MANAGE_CREATESUPERUSER = 'createsuperuser'
MANAGE_GET_PATH = 'path'

TETHYS_COMMANDS = [MANAGE_START, MANAGE_COLLECTSTATIC, MANAGE_COLLECTWORKSPACES, MANAGE_COLLECT,
                   MANAGE_CREATESUPERUSER, MANAGE_GET_PATH]
DJANGO_COMMANDS = [i for i in get_django_manage_commands() if i not in TETHYS_COMMANDS]

def add_manage_parser(subparsers):
    # Setup start server command
    manage_parser = subparsers.add_parser('manage', help='Management commands for Tethys Platform.')
    manage_parser.add_argument('command', help='Management command to run.',
                               choices=[*TETHYS_COMMANDS, *DJANGO_COMMANDS])
    manage_parser.add_argument('-m', '--manage', help='Absolute path to manage.py for Tethys Platform installation.')
    manage_parser.add_argument('-p', '--port', type=str,
                               help='Host and/or port on which to bind the development server.')
    manage_parser.add_argument('--noinput', action='store_true',
                               help='Pass the --noinput argument to the manage.py command.')
    manage_parser.add_argument('-f', '--force', required=False, action='store_true',
                               help='Used only with {} to force the overwrite the app directory into its collect-to '
                                    'location.')
    manage_parser.add_argument('-l', '--link', required=False, action='store_true',
                               help='Only used with collectstatic command. Link static directory to STATIC_ROOT '
                                    'instead of copying it. Not recommended.')
    manage_parser.add_argument('--django-help', action='store_true',
                               help='Display the help for specific scommands coming from Django. '
                               'E.g. "tethys manage <django command> --django-help"')
    manage_parser.set_defaults(func=manage_command, which='tethys_manage_command')


def manage_command(args, django_args=""):
    """
    Management commands.
    """
    # Get the path to manage.py
    manage_path = get_manage_path(args)

    # Define the process to be run
    primary_process = None

    if args.command == MANAGE_START:
        if args.port:
            primary_process = ['python', manage_path, 'runserver', args.port]
        else:
            primary_process = ['python', manage_path, 'runserver']

    elif args.command == MANAGE_COLLECTSTATIC:
        # Run pre_collectstatic
        intermediate_process = ['python', manage_path, 'pre_collectstatic']

        if args.link:
            intermediate_process.append('--link')

        run_process(intermediate_process)

        # Setup for main collectstatic
        primary_process = ['python', manage_path, 'collectstatic']

        if args.noinput:
            primary_process.append('--noinput')

    elif args.command == MANAGE_COLLECTWORKSPACES:
        # Run collectworkspaces command
        if args.force:
            primary_process = ['python', manage_path, 'collectworkspaces', '--force']
        else:
            primary_process = ['python', manage_path, 'collectworkspaces']

    elif args.command == MANAGE_COLLECT:
        # Convenience command to run collectstatic and collectworkspaces
        # Run pre_collectstatic
        intermediate_process = ['python', manage_path, 'pre_collectstatic']
        run_process(intermediate_process)

        # Setup for main collectstatic
        intermediate_process = ['python', manage_path, 'collectstatic']

        if args.noinput:
            intermediate_process.append('--noinput')

        run_process(intermediate_process)

        # Run collectworkspaces command
        primary_process = ['python', manage_path, 'collectworkspaces']

    elif args.command == MANAGE_CREATESUPERUSER:
        primary_process = ['python', manage_path, 'createsuperuser']

    elif args.command == MANAGE_GET_PATH:
        primary_process = ['python', '-c', f'print("{manage_path}")']

    elif args.command in DJANGO_COMMANDS:
        if args.django_help:
            primary_process = ['python', manage_path, args.command, '--help']
        else:
            primary_process = ['python', manage_path, args.command, *django_args]

    if primary_process:
        run_process(primary_process)
