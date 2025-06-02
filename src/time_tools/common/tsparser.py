# flake8: noqa: E501
#
#   (C) Sebastian Weigmann, 2025
#   This software is released under:
#   GNU GENERAL PUBLIC LICENSE, Version 3
#   Please find the full text in LICENSE.
#
# generic imports
import re

def tsparse(ts: str) -> str:
    # TODO: Make this much much better!
    myts = ts
    # deal with some common non-parsable time formats
    # TODO: Make this a dict to include transformation sytax
    list_ts_formats: list[re.Pattern] = []
    # Apache logs: 18/Sep/2011:19:18:28 -0400
    regex_apache_logs = r"(\d{2})/([a-zA-Z]{3})/(\d{4}):(\d{2}):(\d{2}):(\d{2}) ([+-]\d{4})"
    rec = re.compile(regex_apache_logs)
    recm = rec.match(myts)
    if recm:
        newts = f"{recm.group(1)}/{recm.group(2)}/{recm.group(3)} {recm.group(4)}:{recm.group(5)}:{recm.group(6)} {recm.group(7)}"
    else:
        newts = myts
    return newts
