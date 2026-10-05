
import sqlite3
import re
from pathlib import Path


DATABASE_FILE = Path("data/coa_architects.db")


def get_registration_year(registration_number):
    """
    Extract year from registration number.

    Example:
    CA/1990/13290 -> 1990
    """

    if not registration_number:
        return None

    match = re.search(
        r"CA/(\d{4})/",
        registration_number
    )

    if match:
        return int(match.group(1))

    return None


def get_pincode(address):
    """
    Extract 6-digit Indian pincode.
    """

    if not address:
        return None

    match = re.search(
        r"\b\d{6}\b",
        address
    )

    if match:
        return match.group(0)

    return None


def get_city(address):
    """
    Extract city from the address.

    The COA addresses generally contain:
    ..., City, STATE - PINCODE
    """

    if not address:
        return None

    match = re.search(
        r",\s*([^,]+),\s*[A-Z\s]+-\s*\d{6}",
        address
    )

    if match:
        return match.group(1).strip()

    return None


def get_state(address):
    """
    Extract state from:
    STATE - PINCODE
    """

    if not address:
        return None

    match = re.search(
        r",\s*([A-Z\s]+)-\s*\d{6}",
        address
    )

    if match:
        return match.group(1).strip()

    return None


def clean_phone(phone):
    """
    Keep digits only.
    """

    if not phone:
        return None

    digits = re.sub(
        r"\D",
        "",
        phone
    )

    return digits if digits else None


def clean_email(email):
    """
    Remove extra spaces and convert email to lowercase.
    """

    if not email:
        return None

    email = email.strip().lower()

    return email if email else None


def main():

    print("Starting data normalization...")

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            registration_number,
            address,
            mobile,
            email
        FROM architects
    """)

    records = cursor.fetchall()

    updated = 0

    for record in records:

        (
            record_id,
            registration_number,
            address,
            mobile,
            email
        ) = record

        registration_year = get_registration_year(
            registration_number
        )

        city = get_city(address)

        state = get_state(address)

        pincode = get_pincode(address)

        phone = clean_phone(mobile)

        cleaned_email = clean_email(email)

        cursor.execute("""
            UPDATE architects
            SET
                registration_year = ?,
                city = ?,
                state = ?,
                pincode = ?,
                phone = ?,
                email = ?
            WHERE id = ?
        """, (
            registration_year,
            city,
            state,
            pincode,
            phone,
            cleaned_email,
            record_id
        ))

        updated += 1

    connection.commit()

    connection.close()

    print(f"Records normalized: {updated}")
    print("Normalization completed.")


if __name__ == "__main__":
    main()
