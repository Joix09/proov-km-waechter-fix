# km_wachter.py
# KM-Waechter decides when a Vossberg Mobility car needs a service.
# Written in 2013. Modernized 2025.

SERVICE_INTERVAL_KM: int = 15000
WARN_AT_PERCENT: int = 80


def wear_percent(km_since_service: float, interval: int) -> float:
    """Return how much of one service interval has been consumed, as a percentage (0–100+)."""
    return km_since_service / interval * 100


def needs_service(car: dict) -> bool:
    """Return True if the car has reached the warning threshold and is due for service.

    A car with no last_service_km reading cannot be evaluated and is NOT flagged.
    """
    last = car.get("last_service_km")
    if last is None:
        return False
    pct = wear_percent(car["odometer"] - last, SERVICE_INTERVAL_KM)
    return pct >= WARN_AT_PERCENT


def check_fleet(fleet: list) -> list:
    """Flag every car in the fleet that is due for service and return their IDs."""
    flagged = []
    for car in fleet:
        if needs_service(car):
            flagged.append(car["id"])
            print(f"SERVICE DUE: {car['id']}")
    return flagged
