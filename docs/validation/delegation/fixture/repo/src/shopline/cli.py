import argparse
import sys

from shopline import orders


def _cmd_cancel(args) -> int:
    print(f"cancel requested for {args.order_id}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="shopline")
    sub = parser.add_subparsers(dest="command", required=True)
    cancel = sub.add_parser("cancel", help="cancel an order")
    cancel.add_argument("order_id")
    cancel.set_defaults(handler=_cmd_cancel)
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.handler(args)


if __name__ == "__main__":
    sys.exit(main())
