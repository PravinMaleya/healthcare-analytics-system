from pathlib import Path

from database.db_connection import get_connection


CSV_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "processed"
    / "cleaned_healthcare.csv"
)


# Load the cleaned healthcare CSV into PostgreSQL.
def load_healthcare_data():
    print("1. Starting loader...", flush=True)
    print(f"2. CSV exists: {CSV_PATH.exists()}", flush=True)

    print("3. Connecting to PostgreSQL...", flush=True)

    with (
        get_connection() as connection,
        connection.cursor() as cursor,
        CSV_PATH.open("r", encoding="utf-8") as file,
    ):
        print("4. Connected and CSV opened.", flush=True)
        print("5. Starting COPY...", flush=True)

        with cursor.copy(
            """
            COPY healthcare (
                name, age, gender, blood_type,
                medical_condition, date_of_admission,
                doctor, hospital, insurance_provider,
                billing_amount, room_number, admission_type,
                discharge_date, medication, test_results
            )
            FROM STDIN
            WITH (FORMAT CSV, HEADER TRUE, NULL '')
            """
        ) as copy:
            while data := file.read(8192):
                copy.write(data)

        print("6. COPY finished.", flush=True)
        connection.commit()
        print("7. Transaction committed.", flush=True)

    print("Healthcare data loaded successfully.", flush=True)
    
if __name__ == "__main__":
    load_healthcare_data()