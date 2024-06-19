import argparse


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    init_parser = subparsers.add_parser('init')

    create_parser = subparsers.add_parser('connect')

    args = parser.parse_args()

    if args.command == 'test':
        print("test")
    else:
        print("Invalid command. Please follow the usage below.")
        print("Usage: cela <command>")


if __name__ == '__main__':
    main()
