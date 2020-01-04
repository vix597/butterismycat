'''
Helpful utilities for butterismycat
'''
import os
import sys
import random
import logging

logger = logging.getLogger(__name__)


class ArgHider:
    '''
    Allows us to pass args to django that have custom args
    that django doesn't know about without it crashing.
    Similar to django custom commands, but for more basic stuff.
    '''

    _instance = None

    def __init__(self):
        self.args = list(sys.argv)
        self.is_help = False
        self.configure(
            help_text="""ButterIsMyCat.com Server
    --production - Run in production mode (DEBUG=False) with a generated SECRET_KEY""",
            flags=["--production"],
            args=[]
        )

    @staticmethod
    def _strip_arg(arg):
        '''
        Strip off the '-' for the arg
        '''
        return arg.replace('-', '')

    def configure(self, help_text="", flags=None, args=None):
        '''
        Configure the arg hider with the arguments to find and hide.
        flags are args without a parameter. Args have a parameter
        '''
        flags = flags or []
        args = args or []

        for flag in flags:
            setattr(self, ArgHider._strip_arg(flag), False)
        for arg in args:
            setattr(self, ArgHider._strip_arg(arg), None)

        new_args = []
        skip_next = False
        for i in range(len(self.args)):
            if skip_next:
                skip_next = False
                continue

            arg = self.args[i]
            stripped = ArgHider._strip_arg(arg)
            if hasattr(self, stripped) and arg in flags:
                setattr(self, stripped, True)
            elif hasattr(self, stripped) and arg in args and len(self.args) >= (i + 1):
                setattr(self, stripped, self.args[i + 1])
                skip_next = True
            else:
                new_args.append(arg)

        self.args = new_args

        if help_text and "-h" in self.args or "--help" in self.args or "help" in self.args:
            print(help_text)
            self.is_help = True
            self.args = [self.args[0], "help"]

    @classmethod
    def create(cls):
        '''
        Create an instance of the ArgHider
        '''
        hdr = cls()
        ArgHider._instance = hdr
        return hdr

    @classmethod
    def get(cls):
        '''
        Get or create an instance of the ArgHider
        '''
        return cls._instance or cls.create()

    def __iter__(self):
        '''
        Return an iterator for args meant for django
        '''
        return iter(self.args)

    def __getitem__(self, index):
        '''
        Only allow access to args that are meant for django
        '''
        return self.args[index]

    def __len__(self):
        '''
        Get len of django args
        '''
        return len(self.args)


def generate_secret_key_file(path):
    '''
    Generate the secret key/file
    '''
    k = ''.join(random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50))
    try:
        with open(path, 'w') as f:
            f.write(k)
    except Exception as e:
        print("Unable to create secret key file: ", str(e))
        sys.exit(-1)

    return k


def read_secret_key(path):
    '''
    Load the secret key from a file
    '''
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        print("Unable to load secret key from file: ", str(e))
        sys.exit(-1)


def get_secret_key(path):
    '''
    Handles getting the secret key in production/debug mode
    '''
    args = ArgHider.get()

    if args.production:
        print("Production mode enabled!")

        if not os.path.exists(path):
            print("Secret key file {} not found. Creating...".format(path))
            return generate_secret_key_file(path)

        print("Loading secret key from file {}.".format(path))
        return read_secret_key(path)

    # SECURITY WARNING: don't run with debug turned on in production!
    print("WARNING!! RUNNING IN DEBUG MODE. SECRET KEY IS NOT SECURE.")
    print("WARNING!! RUNNING IN DEBUG MODE. SECRET KEY IS NOT SECURE.")
    print("WARNING!! RUNNING IN DEBUG MODE. SECRET KEY IS NOT SECURE.")
    print("This better not be production!")
    print("To run the server in production mode use the '--production' argument.")

    return "DEBUG_SECRET_KEY_DONT_EVER_USE_THIS"
