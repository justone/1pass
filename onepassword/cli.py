import argparse
from getpass import getpass
import os
import sys

from onepassword import Keychain

DEFAULT_KEYCHAIN_PATH = "~/Dropbox/1Password.agilekeychain"

class CLI(object):
    def __init__(self, arguments):
        self.arguments = self.argument_parser().parse_args(arguments)

    def run(self):
        keychain = Keychain(self.arguments.path)
        while keychain.locked:
            try:
                keychain.unlock(getpass("Master password: "))
            except KeyboardInterrupt:
                print("")
                sys.exit(0)

        if self.arguments.fuzzy:
            item = keychain.item(self.arguments.item, fuzzy_threshold=70)
        else:
            item = keychain.item(self.arguments.item)

        if item is not None:
            print(item.password)
        else:
            sys.stderr.write("Could not find a item named '%s'\n" % self.arguments.item)
            sys.exit(1)

    def argument_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("item", help="The name of the password to decrypt")
        parser.add_argument(
            "--path",
            default=os.environ.get('ONEPASSWORD_KEYCHAIN', DEFAULT_KEYCHAIN_PATH),
            help="Path to your 1Password.agilekeychain file",
        )
        parser.add_argument(
            "--fuzzy",
            action="store_true",
            help="Perform fuzzy matching on the item",
        )
        return parser
