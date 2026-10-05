
from pathlib import Path
from bs4 import BeautifulSoup
import csv


INPUT_FILE = Path("data/coa_search_results.html")
OUTPUT_FILE = Path("data/architect_results.csv")


def main():

    print("Reading saved COA result page...")

    # Check whether HTML file exists
    if not INPUT_FILE.exists():

        print(
            f"ERROR: File not found: {INPUT_FILE}"
        )

        return

    # Read HTML
    html = INPUT_FILE.read_text(
        encoding="utf-8"
    )

    print(
        f"HTML size: {len(html)} characters"
    )

    # Parse HTML
    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    # Find tables
    tables = soup.find_all("table")

    print(
        f"Tables found: {len(tables)}"
    )

    if not tables:

        print("No tables found.")

        return

    rows = []

    # Examine tables
    for table_number, table in enumerate(
        tables,
        start=1
    ):

        print(
            f"\nChecking table {table_number}..."
        )

        for tr in table.find_all("tr"):

            cells = tr.find_all(
                ["th", "td"]
            )

            values = [
                cell.get_text(
                    " ",
                    strip=True
                )
                for cell in cells
            ]

            if values:

                print(values)

                # Architect result table
                if len(values) == 7:

                    # Skip header row
                    if values[0].lower() != "s.no":

                        rows.append(values)

    print(
        f"\nArchitect rows found: {len(rows)}"
    )

    # Save CSV
    if rows:

        headers = [
            "S.No",
            "Architect Name",
            "Registration Number",
            "Disciplinary Action",
            "Address",
            "Mobile",
            "Email ID"
        ]

        with OUTPUT_FILE.open(
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            writer = csv.writer(file)

            writer.writerow(headers)
            writer.writerows(rows)

        print(
            f"\nCSV saved successfully:"
        )

        print(OUTPUT_FILE)

    else:

        print(
            "\nNo architect rows were found."
        )


if __name__ == "__main__":
    main()

