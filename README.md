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

### ts_to_isoutc:

This is a real simple tool that accepts one single timestamp and writes the
converted output to `stdout`. As such, it is intended to be used within a
piped chain of commands or within scripted loops.

#### example:

Timestamp values as input below will yield these results:

| original timestamp                  | converted timestamp (ISO-8601 UTC) | notes                                                                                                                                                          |
|-------------------------------------|------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `2021-11-01T13:26:06+01:00`         | `2021-11-01T12:26:06+00:00`        |                                                                                                                                                                |
| `"Nov 26 09:12:30"`                 | `2025-11-26T08:12:30+00:00`        | Assumes timestamp TZ == system TZ                                                                                                                              |
| `"2021-11-18 09:20:37"`             | `2021-11-18T08:20:37+00:00`        | Assumes timestamp TZ == system TZ                                                                                                                              |
| `"Fri 26 Nov 2021 04:58:00 AM CST"` | `2021-11-26T10:58:00+00:00`        | This is NOT the Chinese Standard Time! If you would like Asia/Taipei time, you would need to use `CSTTW` as TZ as defined in `time_tools/common/tzmapping.py`. |
| `"Fri May  2 15:06:24 CEST 2025"`   | `2025-05-02T13:06:24+00:00`        | Input was taken from `LANG=en_US date`. Parsing will fail if input is not in en_US format.                                                                     |
