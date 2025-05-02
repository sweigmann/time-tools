#!/usr/bin/env python3
# flake8: noqa: E501
import pytest      # noqa: F401
import subprocess
import os


class Test_ts_to_isoutc(object):
    # end-to-end tests
    tests = [
        {"input": "2021-11-01T13:26:06+01:00",          "output": "2021-11-01T12:26:06+00:00"},
        {"input": "Nov 26 09:12:30 CEST",               "output": "2025-11-26T08:12:30+00:00"},
        {"input": "2021-11-18 09:20:37 CEST",           "output": "2021-11-18T08:20:37+00:00"},
        {"input": "Fri 26 Nov 2021 04:58:00 AM CST",    "output": "2021-11-26T10:58:00+00:00"},
        {"input": "Fri May  2 15:06:24 CEST 2025",      "output": "2025-05-02T13:06:24+00:00"}
    ]

    def test_process(self):
        p = subprocess.run(
            ["python3", os.path.join("src", "time_tools", "ts_to_isoutc.py"), "--help"],
            capture_output=True,
            text=True,
            check=True,
            timeout=5,
        )
        assert p.returncode == 0
        assert "usage: ts_to_isoutc (time-tools) [-h] " in p.stdout

    def test_timestamps(self):
        for t in Test_ts_to_isoutc.tests:
            ts_in = t.get("input")
            ts_out = t.get("output")
            p = subprocess.run(
                ["python3", os.path.join("src", "time_tools", "ts_to_isoutc.py"), ts_in],
                capture_output=True,
                text=True,
                check=True,
                timeout=5,
            )
            assert p.returncode == 0
            assert p.stdout.strip() == ts_out

    def test_timestamps_zulu(self):
        for t in Test_ts_to_isoutc.tests:
            ts_in = t.get("input")
            ts_out = t.get("output")
            p = subprocess.run(
                ["python3", os.path.join("src", "time_tools", "ts_to_isoutc.py"), "-z", ts_in],
                capture_output=True,
                text=True,
                check=True,
                timeout=5,
            )
            assert p.returncode == 0
            assert p.stdout.strip() == ts_out.replace("+00:00", "Z")
