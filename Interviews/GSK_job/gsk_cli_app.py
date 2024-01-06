import argparse
import sys
from datetime import timedelta, datetime
import re
from functools import partial


HEX7_PATTERN = re.compile(r"^[\dabcdef]{7}$")
EMAIL_PATTERN = re.compile(r"^[a-z]+\.[a-z]\.[a-z]+@gsk\.com")


def valid_job_time(x: str) -> timedelta:
    err_msg = "Time is invalid, expected one of the formats: DD-HH:MM, HH:MM:SS, or MM"
    try:
        "DD-HH:MM", "HH:MM:SS", "MM"
        if len(x) == 2:
            m = int(x)
            if m > 0 and m < 60:
                return timedelta(minutes=m)
        elif len(x) == 8:
            if x[2] == "-":
                return timedelta(days=int(x[0:2]), hours=int(x[3:5]), minutes=int(x[6:8]))
            else:
                # just an error check, a complicated regex would be better but I lack time
                _ = datetime.strptime(x, "%H:%M:%S")
                v = [int(z) for z in x.split(":")]
                return timedelta(hours=v[0], minutes=v[1], seconds=v[2])
    except ValueError:
        True == True
    raise argparse.ArgumentTypeError(err_msg)


def ranged_int(x: str, min_val: int = None, max_val: int = None) -> int:
    err_msg = "Value must be an integer"
    try:
        i = int(x)
        if min_val is not None:
            if i < min_val:
                err_msg += f" >= {min_val}"
                raise argparse.ArgumentTypeError(err_msg)
        if max_val is not None:
            if i > max_val:
                err_msg += f" <= {max_val}"
                raise argparse.ArgumentTypeError(err_msg)
        return i
    except ValueError:
        raise argparse.ArgumentTypeError(err_msg)


def formatted_str(x: str, pattern: re.Pattern = None) -> str:
    if x and pattern is None or pattern.match(x):
        return x
    raise argparse.ArgumentTypeError(
        "Value must be a non-empty string" + ("" if pattern is None else f" of form: {pattern.pattern}")
    )


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument("--job-time", type=valid_job_time, required=True)
    parser.add_argument("--job-name", type=str, required=False)
    parser.add_argument("--cpu-core-count", type=partial(ranged_int, min_val=1, max_val=99), default=4)

    parser.add_argument("--commit-hash", type=partial(formatted_str, pattern=HEX7_PATTERN), required=True)
    parser.add_argument("--gsk-email", type=partial(formatted_str, pattern=EMAIL_PATTERN), required=True)
    parser.add_argument("--verbose", type=bool, required=False, default=False)

    return parser


if __name__ == "__main__":
    # Redirection needed to check invalid arg cases
    sys.stderr = sys.stdout

    # input_str = input()
    # split_input = input_str.split()
    # sys.argv = split_input

    parser = create_parser()
    try:
        args = parser.parse_args()
    except SystemExit:
        sys.exit(0)

    print(args)
