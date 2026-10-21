# config_loader.py
# Reads settings.cfg.
# Written in 2013. Modernized 2025: file handle safety, None comparison fixed.

SETTINGS_FILE: str = "settings.cfg"

KNOWN_KEYS: list = [
    "service_interval_km",
    "warn_at_percent",
    "report_title",
    "history_file",
    "log_file",
    "mileage_unit",
]


def load_settings(path: str | None = None) -> dict:
    """Load key=value pairs from the settings file. Unknown keys are ignored."""
    if path is None:
        path = SETTINGS_FILE
    settings: dict = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            if key in KNOWN_KEYS:
                settings[key] = value
    return settings


def get_int(settings: dict, key: str, fallback: int) -> int:
    """Return an integer value from settings, or fallback if missing or non-numeric."""
    if key in settings:
        try:
            return int(settings[key])
        except ValueError:
            return fallback
    return fallback


def get_setting(settings: dict, key: str, fallback: str = "") -> str:
    """Return a string value from settings, or fallback if the key is absent."""
    return settings.get(key, fallback)
