#!/usr/bin/env python

"""Tests for `codebots` package."""

import pytest

from click.testing import CliRunner
import codebots.cli.cli

bots = ['main',
        'latexbot',
        'sshbot',
        'deploybot',
        'drivebot',
        'telebot',
        'slackbot',
        'emailbot']


def test_bots():
    for bot in bots:
        runner = CliRunner()
        result = runner.invoke(getattr(codebots.cli.cli, bot))
        assert result.exit_code == 0
