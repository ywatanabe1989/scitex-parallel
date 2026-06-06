#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for wait_key and _return_counting_process.

We don't actually press keys — instead we monkey-patch ``readchar`` so
the wait loop exits deterministically. The process-terminate path is
exercised by a stub object.
"""
from __future__ import annotations

import sys
import types

import pytest

from scitex_parallel import _return_counting_process, wait_key


class _StubProcess:
    def __init__(self):
        self.terminated = False

    def terminate(self):
        self.terminated = True


@pytest.fixture
def fake_readchar(monkeypatch):
    """Yield a chars-list that readchar.readchar() will return one-at-a-time."""
    state = {"chars": []}

    def reader():
        return state["chars"].pop(0)

    fake = types.SimpleNamespace(readchar=reader)
    monkeypatch.setitem(sys.modules, "readchar", fake)
    return state


class TestWaitKey:
    def test_default_key_is_q(self, fake_readchar, capsys):
        fake_readchar["chars"] = ["a", "b", "q"]
        proc = _StubProcess()
        wait_key(proc)
        assert proc.terminated is True

    def test_custom_key(self, fake_readchar, capsys):
        fake_readchar["chars"] = ["x", "y", "z"]
        proc = _StubProcess()
        wait_key(proc, key="z")
        assert proc.terminated is True

    def test_echoes_keystrokes(self, fake_readchar, capsys):
        fake_readchar["chars"] = ["a", "q"]
        wait_key(_StubProcess())
        captured = capsys.readouterr()
        assert "a" in captured.out
        assert "q" in captured.out


class TestReturnCountingProcess:
    def test_spawns_and_terminates(self):
        p = _return_counting_process()
        try:
            assert p.is_alive()
        finally:
            p.terminate()
            p.join(timeout=2)
