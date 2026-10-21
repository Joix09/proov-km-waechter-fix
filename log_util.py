# log_util.py
# A simple timestamped logger.
# Written in 2013. Modernized 2025.

import time

LOG_LINES: list = []   # global buffer shared by all importers; cleared after each flush
DEBUG: bool = False


def log(message: str) -> None:
    """Append a timestamped line to the in-memory log buffer and print it."""
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"
    LOG_LINES.append(line)
    print(line)


def debug(message: str) -> None:
    """Log a DEBUG-level message. No-op unless DEBUG is set to True."""
    if DEBUG:
        log(f"DEBUG: {message}")


def flush_log(path: str) -> None:
    """Write all buffered log lines to the log file and clear the buffer."""
    with open(path, "a") as f:
        for line in LOG_LINES:
            f.write(line + "\n")
    LOG_LINES.clear()
