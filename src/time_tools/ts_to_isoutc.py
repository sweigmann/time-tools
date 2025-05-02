# flake8: noqa: E501
# This is ts_to_isoutc for converting many kinds of timestamps
# to UTC in ISO-8601.
#   (C) Sebastian Weigmann, 2025
#   This software is released under:
#   GNU GENERAL PUBLIC LICENSE, Version 3
#   Please find the full text in LICENSE.
#
# Exit codes:
#   0:  all good
#   1:  generic error
#   2:  argument parser error
#
#
# generic imports
import datetime
import sys
import argparse

# specific imports
from dateutil import tz
from dateutil import parser as duparser
try:
    from common import errors as ERR
    from common import version
    from common.tzmapping import tzmapping
except ModuleNotFoundError:
    from time_tools.common import errors as ERR
    from time_tools.common import version
    from time_tools.common.tzmapping import tzmapping


# global variables
my_progname = "ts_to_isoutc"
my_progver = "1"
progname = my_progname + " (" + version.progname + ")"
progver = version.progver + "-" + my_progver
ERR.verbosity = 0


def parse_args() -> argparse.Namespace:
    global progname
    global progver
    parser = argparse.ArgumentParser(
        prog=progname,
        description="Convert a variety of timestamps to UTC ISO-8601",
#        epilog="",
    )
    parser.add_argument(
        "--use-zulu",
        "-z",
        action="store_true",
        help="replace \"+00:00\" with \"Z\"",
    )
#    parser.add_argument(
#        "--verbose",
#        "-v",
#        action="count",
#        default=0,
#        help="can be given multiple times to increase verbosity",
#    )
    parser.add_argument("--version", action="version", version="%(prog)s v" + progver)
    parser.add_argument(
        "timestamp",
        help="timestamp to be converted",
    )
    try:
        args = parser.parse_args()
        return args
    except Exception as excpt:
        # we get here when anything is wrong with provided arguments. fail and exit.
        ERR.printmsg(f"{type(excpt).__name__}: {excpt}", ERR.ERRLVL.CRIT)
        sys.exit(ERR.EXIT.ARGPARSE)


def __main() -> None:
    global progname
    global progver
    ERR.verbosity = ERR.ERRLVL.DEBUG
    args = parse_args()
    try:
        mytime = args.timestamp
        datetime_obj = duparser.parse(mytime, tzinfos=tzmapping)
        utcdatetime_obj = datetime_obj.astimezone(datetime.timezone.utc)
        isoutc_timestamp = utcdatetime_obj.isoformat(timespec="seconds")
        if args.use_zulu:
            isoutc_timestamp = isoutc_timestamp.replace("+00:00", "Z")
        print(isoutc_timestamp)
    except:
        ERR.printmsg(f"Unable to convert timestamp: {args.timestamp}", ERR.ERRLVL.ERROR)
    return


def main() -> None:
    try:
        __main()
    except Exception as main_excpt:
        # yeah, this is truly unexpected. ever got CTRL+C'ed?? bail the heck out!
        ERR.printmsg(f"{type(main_excpt).__name__}: {main_excpt}", ERR.ERRLVL.CRIT)
        sys.stderr.flush()
        sys.stdout.flush()
        sys.exit(ERR.EXIT.GENERIC)
    sys.exit(ERR.EXIT.OK)


# void main() { do stuff }
if __name__ == "__main__":
    main()
