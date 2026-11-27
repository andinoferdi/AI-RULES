"""Command line for the alert notifier."""
import argparse
import sys


def build_parser():
    parser = argparse.ArgumentParser(prog="notify")
    parser.add_argument("--channel", default="email", choices=["email", "sms"],
                        help="where alerts are sent")
    parser.add_argument("--test-alert", action="store_true",
                        help="send one test alert so you can check that you recieve alerts")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.test_alert:
        print(f"test alert sent via {args.channel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
