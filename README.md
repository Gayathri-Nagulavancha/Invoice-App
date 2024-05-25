Invoice Management API
This project is a RESTful API for managing a simple invoice system. It is built using Python, FastAPI, and PostgreSQL. The API supports creating, reading, updating, and deleting invoice records.

Features :
Create Invoice: Add new invoices to the database.
Get All Invoices: Retrieve a list of all invoices.
Get Invoice by ID: Retrieve a specific invoice by its ID.
Update Invoice: Modify an existing invoice.
Delete Invoice: Remove an invoice from the database.
Validation: Ensure data integrity using Pydantic models.
Error Handling: Handle invalid data and database errors gracefully.

Requirements : Python 3.8+
PostgreSQL
FastAPI
SQLAlchemy
Pydantic

Project Structure
.
├── main.py           # Main application file
├── database.py       # Database configuration
├── models.py         # SQLAlchemy models
├── create_db.py      # Script to create database tables
└── README.md         # Project documentation

Setup and Installation
1. Clone the Repository
2. Create a Virtual Environment and Install Dependencies
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
3. Configure the Database
Ensure you have PostgreSQL installed and running. Update the SQLALCHEMY_DATABASE_URL in database.py with your database credentials:
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://username:password@localhost/invoice"
4. Create Database Tables
Run the following script to create the necessary tables:
python create_db.py
5. Run the Application
Start the FastAPI server:
uvicorn main:app --reload
The application will be available at http://127.0.0.1:8000. 
