# time-tools

Collection of tools to handle timestamps

<img src="https://github.com/sweigmann/time-tools/actions/workflows/codeql-analysis.yml/badge.svg?branch=main">
<img src="https://github.com/sweigmann/time-tools/actions/workflows/python-linux.yml/badge.svg?branch=main">
<img src="https://github.com/sweigmann/time-tools/actions/workflows/debian.yml/badge.svg?branch=main">
<img src="https://github.com/sweigmann/time-tools/actions/workflows/ubuntu.yml/badge.svg?branch=main">

## installation:

```bash
pipx install git+https://codeberg.org/DFIR/time-tools.git
```

## usage:

### ts_to_iso_utc:

```commandline
usage: ts_to_iso_utc [-h] [-z] [--version] {convert,subts,subsecs,addsecs} ...
```

This is a tool for timestamp conversion and subtraction, as well as delta
subtraction and addition from and to timestamps.

Output is written to `stdout`. As such, it is intended to be used within a
piped chain of commands or within scripted loops.

#### examples:

##### timestamp conversion:

Timestamp values as input below will yield these results after conversion (command: `convert`).

| original timestamp                  | converted timestamp (ISO-8601 UTC) | notes                                                                                                                                                          |
|-------------------------------------|------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `2021-11-01T13:26:06+01:00`         | `2021-11-01T12:26:06+00:00`        |                                                                                                                                                                |
| `"2025 Nov 26 09:12:30"`            | `2025-11-26T08:12:30+00:00`        | Assumes timestamp TZ == system TZ                                                                                                                              |
| `"2021-11-18 09:20:37"`             | `2021-11-18T08:20:37+00:00`        | Assumes timestamp TZ == system TZ                                                                                                                              |
| `"Fri 26 Nov 2021 04:58:00 AM CST"` | `2021-11-26T10:58:00+00:00`        | This is NOT the Chinese Standard Time! If you would like Asia/Taipei time, you would need to use `CSTTW` as TZ as defined in `time_tools/common/tzmapping.py`. |
| `"Fri May  2 15:06:24 CEST 2025"`   | `2025-05-02T13:06:24+00:00`        | Input was taken from `LANG=en_US date`. Parsing will fail if input is not in en_US format.                                                                     |

##### subtracting timestamps from each other:

This use case will allow you to calculate the delta in seconds for two given
timestamps, for example to calculate the offset between two timelines from
different artifacts.

| younger timestamp                   | older timestamp               | command | delta [s]      |
|-------------------------------------|-------------------------------|---------|----------------|
| `"Fri 26 Nov 2021 04:58:00 AM CST"` | `"2025 Jun 26 09:12:30 CEST"` | `subts` |  `112997670.0` |

##### subtracting or adding a delta from or to a timestamp:

Time correction on artifacts requires a known offset to be added or subtracted
to or from a timeline in order to be correlated to the master timeline.

| original timestamp                  | offset [s] | command   | corrected timestamp (ISO-8601 UTC) |
|-------------------------------------|------------|-----------|------------------------------------|
| `"2025 Jun 26 09:12:30 CEST"`       | `43674`    | `subsecs` | `2025-06-25T19:04:36+00:00`        |
| `"Fri 26 Nov 2021 04:58:00 AM CST"` | `86400`    | `addsecs` | `2021-11-27T10:58:00+00:00`        |
