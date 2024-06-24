import getopt
import sys

from rich import print

from .services import base, role, brand, device_category, device, user, todo


def main(args):
    try:
        opts, args = getopt.getopt(args)
    except getopt.GetoptError:
        print("Usage: cela <command>")
        sys.exit(2)

    if args[1] == 'todo':
        todo.switch(args)
    else:
        print("Invalid command. Please follow the usage below.")
        print("Usage: cela <command>")


if __name__ == '__main__':
    main(sys.argv[1:])
