#!/usr/bin/env python3
# flake8: noqa: E501
import pytest      # noqa: F401
import subprocess
import os


class Test_ts_to_iso_utc(object):
    # end-to-end tests
    delta = "100644"
    tests = [
        {
            "input"     : "2021-11-01T13:26:06+01:00",
            "output"    : "2021-11-01T12:26:06+00:00",
            "minusdelta": "2021-10-31T08:28:42+00:00",
            "plusdelta" : "2021-11-02T16:23:30+00:00"
        },
        {
            "input"     : "2025 Nov 26 09:12:30 CEST",
            "output"    : "2025-11-26T08:12:30+00:00",
            "minusdelta": "2025-11-25T04:15:06+00:00",
            "plusdelta" : "2025-11-27T12:09:54+00:00"
        },
        {
            "input"     : "2021-11-18 09:20:37 CEST",
            "output"    : "2021-11-18T08:20:37+00:00",
            "minusdelta": "2021-11-17T04:23:13+00:00",
            "plusdelta" : "2021-11-19T12:18:01+00:00"
        },
        {
            "input"     : "Fri 26 Nov 2021 04:58:00 AM CST",
            "output"    : "2021-11-26T10:58:00+00:00",
            "minusdelta": "2021-11-25T07:00:36+00:00",
            "plusdelta" : "2021-11-27T14:55:24+00:00"
        },
        {
            "input"     : "Fri May  2 15:06:24 CEST 2025",
            "output"    : "2025-05-02T13:06:24+00:00",
            "minusdelta": "2025-05-01T09:09:00+00:00",
            "plusdelta" : "2025-05-03T17:03:48+00:00"
        }
    ]

    def test_process(self):
        p = subprocess.run(
            ["python3", os.path.join("src", "time_tools", "ts_to_iso_utc.py"), "--help"],
            capture_output=True,
            text=True,
            check=True,
            timeout=5,
        )
        assert p.returncode == 0
        assert "usage: ts_to_iso_utc [-h] [-z] [--version] " in p.stdout

    def test_ts_to_iso_utc_convert(self):
        for t in Test_ts_to_iso_utc.tests:
            ts_in = t.get("input")
            ts_out = t.get("output")
            p = subprocess.run(
                ["python3", os.path.join("src", "time_tools", "ts_to_iso_utc.py"), "convert", ts_in],
                capture_output=True,
                text=True,
                check=True,
                timeout=5,
            )
            assert p.returncode == 0
            assert p.stdout.strip() == ts_out

    def test_ts_to_iso_utc_subts(self):
        ts_older = "Fri 26 Nov 2021 04:58:00 AM CST"
        ts_newer = "2025 Nov 26 09:12:30 CEST"
        expected_result = "126220470.0"
        p = subprocess.run(
            ["python3", os.path.join("src", "time_tools", "ts_to_iso_utc.py"), "subts", ts_older, ts_newer],
            capture_output=True,
            text=True,
            check=True,
            timeout=5,
        )
        assert p.returncode == 0
        assert p.stdout.strip() == expected_result
        try:
            p = subprocess.run(
                ["python3", os.path.join("src", "time_tools", "ts_to_iso_utc.py"), "subts", ts_newer, ts_older],
                capture_output=True,
                text=True,
                check=True,
                timeout=5,
            )
            # We MUST fail here, do not expect retcode Zero!
            assert p.returncode != 0
        except subprocess.CalledProcessError as e:
            assert e.returncode == 1
            assert "CRITICAL: ValueError" in e.stderr.strip()

    def test_ts_to_iso_utc_subsecs(self):
        for t in Test_ts_to_iso_utc.tests:
            ts_in = t.get("input")
            ts_out = t.get("minusdelta")
            p = subprocess.run(
                ["python3", os.path.join("src", "time_tools", "ts_to_iso_utc.py"), "subsecs", ts_in, Test_ts_to_iso_utc.delta],
                capture_output=True,
                text=True,
                check=True,
                timeout=5,
            )
            assert p.returncode == 0
            assert p.stdout.strip() == ts_out

    def test_ts_to_iso_utc_addsecs(self):
        for t in Test_ts_to_iso_utc.tests:
            ts_in = t.get("input")
            ts_out = t.get("plusdelta")
            p = subprocess.run(
                ["python3", os.path.join("src", "time_tools", "ts_to_iso_utc.py"), "addsecs", ts_in, Test_ts_to_iso_utc.delta],
                capture_output=True,
                text=True,
                check=True,
                timeout=5,
            )
            assert p.returncode == 0
            assert p.stdout.strip() == ts_out

    def test_ts_to_iso_utc_zulu(self):
        for t in Test_ts_to_iso_utc.tests:
            ts_in = t.get("input")
            ts_out = t.get("output")
            p = subprocess.run(
                ["python3", os.path.join("src", "time_tools", "ts_to_iso_utc.py"), "-z", "convert", ts_in],
                capture_output=True,
                text=True,
                check=True,
                timeout=5,
            )
            assert p.returncode == 0
            assert p.stdout.strip() == ts_out.replace("+00:00", "Z")
