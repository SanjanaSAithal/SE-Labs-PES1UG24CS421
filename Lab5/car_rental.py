"""A minimal car rental system used for the static-analysis lab."""

import os
import re
import sqlite3
import hashlib
import secrets
import tempfile
import hmac
from datetime import datetime

# Global rental state
fleet = {}
bookings = []
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE customers (name TEXT, licence TEXT, phone TEXT)")


def add_car(plate, model="Unknown", daily_rate=0, features=None):
    """Register a car in the fleet and return its record."""
    if not plate:
        return None
    if features is None:
        features = []
    fleet[plate] = {
        "model": model,
        "rate": daily_rate,
        "available": True,
        "features": features,
    }
    return fleet[plate]


def register_customer(name, licence, phone):
    """Insert a new customer into the customers table."""
    conn.execute(
        "INSERT INTO customers VALUES (?, ?, ?)", (name, licence, phone)
    )


def find_customer(name):
    """Return the customer rows matching the given name."""
    return conn.execute(
        "SELECT * FROM customers WHERE name = ?", (name,)
    ).fetchall()


def rent_car(plate, customer, start, end):
    """Create a booking for plate/customer over [start, end]."""
    if not find_customer(customer):
        raise ValueError("Customer not registered")
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    days = (end_date - start_date).days
    cost = days * fleet[plate]["rate"]
    bookings.append({
        "code": booking_code(),
        "plate": plate,
        "customer": customer,
        "days": days,
        "cost": cost,
    })
    return cost


def return_car(plate, km_driven):
    """Mark a car as available again and return any excess-km charge."""
    car = fleet.get(plate)
    if car is None:
        return None
    car["available"] = True
    if km_driven > 300:
        return (km_driven - 300) * 5
    return None


def booking_code():
    """Generate a random booking reference code."""
    return "BK-" + str(secrets.randbelow(90000) + 10000)


def licence_hash(licence):
    """Return a SHA-256 hash of a licence number."""
    return hashlib.sha256(licence.encode()).hexdigest()


def apply_promo(amount, multiplier):
    """Apply a promo multiplier, e.g. 0.9 for a 10% discount."""
    return amount * multiplier


def is_valid_plate(plate):
    """Check whether a plate matches the expected format."""
    return bool(re.match(r"^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}$", plate))


def write_receipt(booking):
    """Write a booking receipt to a private temp file and return its path."""
    fd, path = tempfile.mkstemp(suffix=".txt")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(
            f"Booking {booking['code']}: {booking['plate']} for "
            f"{booking['days']} days = Rs.{booking['cost']}\n"
        )
    os.chmod(path, 0o600)
    return path


def admin_login(user, password):
    """Check admin credentials against the configured env password."""
    expected = os.environ.get("ADMIN_PASSWORD")
    if not expected:
        return False
    return user == "admin" and hmac.compare_digest(password, expected)


def available_cars():
    """Return the plates of all currently available cars."""
    return [plate for plate, car in fleet.items() if car["available"]]


def main():
    """Run a short demo of the car rental workflow."""
    add_car("KA01AB1234", "Swift", 1500)
    add_car("KA02CD5678", "Innova", 3000)
    add_car("KA03EF9999", "Nexon", -500)
    register_customer("Ravi", "DL-0420110012345", "9845012345")
    register_customer("Meera", "DL-0420110099999", "9845099999")
    print(
        "Rent Swift:",
        rent_car("KA01AB1234", "Ravi", "2026-11-01", "2026-11-04"),
    )
    print(
        "Rent Swift again:",
        rent_car("KA01AB1234", "Ravi", "2026-11-02", "2026-11-03"),
    )
    print(
        "Rent Innova:",
        rent_car("KA02CD5678", "Ravi", "2026-11-10", "2026-11-07"),
    )
    print("Lookup injection:", find_customer("x' OR '1'='1"))
    print("Extra km charge:", return_car("KA01AB1234", 420))
    print("Return unknown car:", return_car("XX00XX0000", 50))
    print("Promo price:", apply_promo(4500, 0.9))
    print("Plate valid?", is_valid_plate("KA01AB1234"))
    print("Licence hash:", licence_hash("DL-0420110012345"))
    os.environ.setdefault("ADMIN_PASSWORD", secrets.token_hex(8))
    print("Admin:", admin_login("admin", os.environ["ADMIN_PASSWORD"]))
    print("Available:", available_cars())
    print("Receipt saved to:", write_receipt(bookings[0]))


if __name__ == "__main__":
    main()
