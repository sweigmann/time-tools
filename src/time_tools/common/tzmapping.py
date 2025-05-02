# flake8: noqa: E501
# This is ts_to_isoutc for converting many kinds of timestamps
# to UTC in ISO-8601.
#   (C) Sebastian Weigmann, 2025
#   This software is released under:
#   GNU GENERAL PUBLIC LICENSE, Version 3
#   Please find the full text in LICENSE.
#
# generic imports
import datetime
import sys

# specific imports
from dateutil import tz


# Timezone mappings
tzmapping = {
    'CET'           :   tz.gettz('Europe/Berlin'),
    'CEST'          :   tz.gettz('Europe/Berlin'),
    'EDT'           :   tz.gettz('America/New_York'),
    'EST'           :   tz.gettz('America/New_York'),
    'CDT'           :   tz.gettz('America/Chicago'),
    'CST'           :   tz.gettz('America/Chicago'),
    'PDT'           :   tz.gettz('America/Los_Angeles'),
    'PST'           :   tz.gettz('America/Los_Angeles'),
    'CSTTW'         :   tz.gettz('Asia/Taipei')
}
