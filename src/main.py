import argparse
import logging
from config import Config


def setup_logging():
    """
    Configure the logging settings
    """
    logging.basicConfig(
        level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    return logging.getLogger(__name__)


def parse_args():
    """
    Parse command-line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help='Debug mode')
    return parser.parse_args()


def check_debug_mode(args, logger):
    """
    Check if debug mode is on, and configure logging accordingly
    """
    if args.debug or Config.DEBUG:
        logger.setLevel(logging.DEBUG)
        logger.debug('Debug mode is on')
    else:
        logger.info('Debug mode is off')


def main():
    # Setup logging
    logger = setup_logging()
    # Parse command-line arguments
    args = parse_args()
    # Check if debug mode is on
    check_debug_mode(args, logger)
    # Print the parsed arguments
    print(args)


if __name__ == '__main__':
    main()
