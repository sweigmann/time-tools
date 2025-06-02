# flake8: noqa: E501
# This is iso-ts_to_isoutc for converting many kinds of timestamps
# to UTC in ISO-8601.
#   (C) Sebastian Weigmann, 2025
#   This software is released under:
#   GNU GENERAL PUBLIC LICENSE, Version 3
#   Please find the full text in LICENSE.
#
# generic imports
import datetime
import sys
import argparse

# specific imports
from dateutil import tz
from dateutil import parser

try:
    from common import tzmapping as TZM
    from common import tsparser as TSP
    from common import version
    from common import errors as ERR
except ModuleNotFoundError:
    from time_tools.common import tzmapping as TZM
    from time_tools.common import tsparser as TSP
    from time_tools.common import errors as ERR
    from time_tools.common import version


# global variables
my_progname = "ts_to_iso_utc"
my_progver = "3"
progname = my_progname + " (" + version.progname + ")"
progver = version.progver + "-" + my_progver
ERR.verbosity = 0


def parse_args() -> argparse.Namespace:
    global progname
    global progver
    epilog = "Examples: " + my_progname + " 2021-11-01T13:26:06+01:00         --> 2021-11-01T12:26:06Z\n" + \
             "          " + my_progname + " \"2025 Nov 26 09:12:30\"                 --> 2021-11-26T09:12:30Z (assumes timestamp TZ is system TZ)\n" + \
             "          " + my_progname + " \"2021-11-18 09:20:37\"             --> 2021-11-18T09:20:37Z (assumes timestamp TZ is system TZ)\n" + \
             "          " + my_progname + " \"Fri 26 Nov 2021 04:58:00 AM CST\" --> NOT Chinese Standard Time! For Taipei time use CSTTW"
    # create the top-level parser
    parser = argparse.ArgumentParser(
        prog=my_progname,
        formatter_class=argparse.RawTextHelpFormatter,
        description="Convert, add and subtract timestamps",
        epilog=epilog
    )
    parser.add_argument("-z", "--use-zulu", dest="z", action='store_true', help='replace "+00:00" by "Z" for Zulu time')
    parser.add_argument("--version", action="version", version="%(prog)s v" + progver)
    # init subparsers
    subparsers = parser.add_subparsers(title="commands", dest="command", required=True)
    # create the parser for "convert"
    parser_convert = subparsers.add_parser('convert', help='convert timestamps to UTC in ISO-8601 format')
    parser_convert.add_argument('ts', type=str, help='timestamp to convert')
    # create the parser for "subts"
    parser_subts = subparsers.add_parser('subts', help='subtract: timestamp - timestamp -> seconds')
    parser_subts.add_argument('ts_younger', type=str, help='timestamp to subtract from')
    parser_subts.add_argument('ts_older', type=str, help='subtractor')
    # create the parser for "subsecs"
    parser_subsecs = subparsers.add_parser('subsecs', help='subtract: timestamp - seconds -> timestamp')
    parser_subsecs.add_argument('ts', type=str, help='timestamp to subtract from')
    parser_subsecs.add_argument('secs', type=float, help='seconds to subtract')
    # create the parser for "addsecs"
    parser_addsecs = subparsers.add_parser('addsecs', help='add: timestamp + seconds -> timestamp')
    parser_addsecs.add_argument('ts', type=str, help='timestamp to add to')
    parser_addsecs.add_argument('secs', type=float, help='seconds to add')
    # parse arguments
    try:
        args = parser.parse_args()
        # make sure we didn't mess up the code.
        return args
    except Exception as excpt:
        # we get here when anything is wrong with provided arguments. fail and exit.
        ERR.printmsg("%s: %s" % (type(excpt).__name__, excpt), ERR.ERRLVL.CRIT)
        sys.exit(ERR.EXIT.ARGPARSE)


def ts_convert(ts: str) -> str:
    datetimeobj = parser.parse(ts, tzinfos=TZM.tzmapping)
    utcdatetimeobj = datetimeobj.astimezone(datetime.timezone.utc)
    isoutctimestamp = utcdatetimeobj.isoformat(timespec="seconds")
    return isoutctimestamp


def ts_sub_ts(ts1: str, ts2: str) -> str:
    datetimeobj1 = parser.parse(ts1, tzinfos=TZM.tzmapping)
    datetimeobj2 = parser.parse(ts2, tzinfos=TZM.tzmapping)
    if datetimeobj2 > datetimeobj1:
        raise ValueError("first timestamp must be older than second timestamp")
    utcdatetimeobj1 = datetimeobj1.astimezone(datetime.timezone.utc)
    utcdatetimeobj2 = datetimeobj2.astimezone(datetime.timezone.utc)
    ts_difference = utcdatetimeobj1 - utcdatetimeobj2
    ERR.printmsg(f"Difference: {ts_difference}", ERR.ERRLVL.DEBUG)
    return str(ts_difference.total_seconds())


def ts_calc_new_ts(ts: str, secs: float, op: str) -> str:
    datetimeobj = parser.parse(ts, tzinfos=TZM.tzmapping)
    utcdatetimeobj = datetimeobj.astimezone(datetime.timezone.utc)
    if op == "add":
        ts_new = utcdatetimeobj + datetime.timedelta(seconds=secs)
    elif op == "sub":
        ts_new = utcdatetimeobj - datetime.timedelta(seconds=secs)
    else:
        raise ValueError("unknown operation")
    ERR.printmsg(f"New TS: {ts_new}", ERR.ERRLVL.DEBUG)
    isoutctimestamp = ts_new.isoformat(timespec="seconds")
    return(isoutctimestamp)


def ts_sub_secs(ts: str, secs: float) -> str:
    return ts_calc_new_ts(ts, secs, "sub")


def ts_add_secs(ts: str, secs: float) -> str:
    return ts_calc_new_ts(ts, secs, "add")


def __main() -> None:
    global progname
    global progver
    ERR.verbosity = ERR.ERRLVL.INFO
    args = parse_args()
    ERR.printmsg(str(args), ERR.ERRLVL.DEBUG)
    result: str = ""
    if args.command == 'convert':
        mytime = TSP.tsparse(args.ts)
        result = ts_convert(mytime)
        if args.z:
            result = result.replace("+00:00", "Z")
    elif args.command == 'subts':
        mytime_o = TSP.tsparse(args.ts_older)
        mytime_y = TSP.tsparse(args.ts_younger)
        result = ts_sub_ts(mytime_o, mytime_y)
    elif args.command == 'subsecs':
        mytime = TSP.tsparse(args.ts)
        result = ts_sub_secs(mytime, args.secs)
        if args.z:
            result = result.replace("+00:00", "Z")
    elif args.command == 'addsecs':
        mytime = TSP.tsparse(args.ts)
        result = ts_add_secs(mytime, args.secs)
        if args.z:
            result = result.replace("+00:00", "Z")
    else:
        # we never should end up here...
        raise ValueError("unknown command")
    # Print plain result to console --> allows command chaining
    print(result)


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
