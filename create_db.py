import models

try:
    models.create_tables()
    print("Tables created successfully.")
except Exception as e:
    print(f"An error occurred: {e}")
