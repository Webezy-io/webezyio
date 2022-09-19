import logging
import argparse
import os

from pathlib import Path

log = logging.getLogger(__name__)

def main(args=None):
    """Main CLI processing, with argpars package.
    """
    print('\n','Webezy.io CLI Started', '\n\n')
    # Main cli parser
    parser = argparse.ArgumentParser(prog='webezy',
                                     description='Command line interface for the webezyio package build awesome gRPC micro-services. For more information please visit https://www.webezy.io there you can find additional documentation and tutorials.',
                                     allow_abbrev=True,
                                     epilog='For more information see - https://www.webezy.io/docs/cli | Created with love by Amit Shmulevitch. 2022 © webezy.io')
    
    # Log level optional argument
    parser.add_argument(
        '--loglevel', default='info', help='Log level',
        choices=['debug', 'info', 'warning', 'error', 'critical', ])

    parser.add_argument(
        'help', action="store_true", help='Log level',
        )

    # Instantiating sub parsers object
    subparsers = parser.add_subparsers(
        help='Main modules to interact with Webezy CLI.')


    # Parse all command line arguments
    args = parser.parse_args(args)

    # This is not a good way to handle the cases
    # where help should be printed.
    # TODO: there must be a better way?
    if hasattr(args, 'func'):
        # Call the desired subcommand function
        logging.basicConfig(level=args.loglevel.upper())
        log.debug(args)
        
        if os.environ.get('WEBEZY_TOKEN') is not None:
            log.debug('Webezy token passed: {0}'.format(os.environ.get('WEBEZY_TOKEN')))
            # TODO verify token
        args.func(args)
        return 0
    else:
        print("Error")
        parser.print_help()
        return 0