import os


class Config:
    # Get the root path of the project
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    # Get the parent directory of the project
    BASE_DIR = os.path.dirname(PROJECT_ROOT)

    # Get the parent directory of the parent directory of the project
    ROOT_DIR = os.path.dirname(BASE_DIR)

    # Get the parent directory of the parent directory of the parent directory of the project
    PARENT_DIR = os.path.dirname(ROOT_DIR)

    # Get the value of the DEBUG environment variable, or False if it's not set
    DEBUG = os.environ.get('DEBUG', False)

    # Get the value of the TESTING environment variable, or False if it's not set
    TESTING = os.environ.get('TESTING', False)

    # Get the value of the SECRET_KEY environment variable, or 'secret' if it's not set
    SECRET = os.environ.get('SECRET_KEY', 'secret')
