#!/usr/bin/env python3
#
# Copyright (C) 2023 Rackslab
#
# This file is part of Slurm-web.
#
# Slurm-web is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Slurm-web is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Slurm-web.  If not, see <https://www.gnu.org/licenses/>.

from typing import List
import logging


def setup_logger(
    formatter: logging.Formatter,
    debug: bool = False,
    flags: List[str] = [],
) -> None:
    if debug:
        logging_level = logging.DEBUG
    else:
        logging_level = logging.INFO

    root_logger = logging.getLogger()
    root_logger.setLevel(logging_level)
    handler = logging.StreamHandler()
    handler.setLevel(logging_level)
    formatter = formatter(debug)
    handler.setFormatter(formatter)
    # filter out all libs logs not enabled in flags
    def custom_filter(record):
        if "ALL" in flags:
            return 1
        if record.name.split(".")[0] not in flags:
            return 0
        return 1

    handler.addFilter(custom_filter)
    root_logger.addHandler(handler)


class ANSIStyle:
    def __init__(self, fg, bg=None):
        self.fg = fg
        self.bg = bg

    @property
    def start(self):
        bg_s = ""
        if self.bg is not None:
            bg_s = f"\033[48;5;{self.bg}m"
        return bg_s + f"\033[38;5;{self.fg}m"

    @property
    def end(self):
        return "\033[0;0m"


LOG_LEVEL_ANSI_STYLES = {
    logging.CRITICAL: ANSIStyle(fg=15, bg=160),  # white on red
    logging.ERROR: ANSIStyle(fg=160),  # red
    logging.WARNING: ANSIStyle(fg=208),  # orange
    logging.INFO: ANSIStyle(fg=28),  # dark green
    logging.DEBUG: ANSIStyle(fg=62),  # light mauve
    logging.NOTSET: ANSIStyle(fg=8),  # grey
}


class TTYFormatter(logging.Formatter):
    def __init__(self, debug=False):
        super().__init__("%(message)s")
        self.debug = debug

    def format(self, record):

        _msg = record.getMessage()
        style = LOG_LEVEL_ANSI_STYLES[record.levelno]
        prefix = ""
        if self.debug:
            prefix = "{level:8s}⸬{where:30s} ↦ ".format(
                level="[" + record.levelname + "]",
                where=record.name + ":" + str(record.lineno),
            )
        elif record.levelno >= logging.INFO:
            # prefix with level if over info
            prefix = "{level} ⸬ ".format(level=record.levelname)

        return style.start + prefix + _msg + style.end
