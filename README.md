# Norman PD Data Extraction README
## Developer Information
Name: Rushang Sunil Chiplunkar

# Assignment Description 
Objective:
The primary goal of this assignment is to practice extracting and processing data from an online source, specifically focusing on incident report PDFs provided by the Norman, Oklahoma Police Department. The task involves downloading these PDFs, extracting relevant information, and then storing this data in a structured format using a SQLite database. This project allowed me to apply my knowledge of Python3, SQL, regular expressions, and Linux command-line tools in a practical scenario.

Tools and Technologies Used:
Python 3.8: The main programming language used for developing the application.
SQLite: A lightweight, file-based database used for storing extracted data.
PyMuPDF (fitz): A Python library for reading PDF documents and extracting text.
Regular Expressions: Utilized for parsing and extracting specific pieces of data from the PDF text.
Linux Command Line: Employed for executing the Python script and managing the file system.

Highlights and Learning Outcomes:
This assignment has been instrumental in enhancing my proficiency in data extraction, processing, and database management. It provided a hands-on experience in applying regular expressions for text parsing, which is a critical skill in data science. Moreover, working with the SQLite database deepened my understanding of SQL and database schema design. Finally, this project underscored the importance of integrating various technologies and tools to solve practical problems in data analysis.

# How to Install
To install and run this project, follow these steps:

1. Clone the repository to your local machine.
2. Ensure you have Python installed. This project was developed with Python 3.8.

## How to Use
To run the program, navigate to the project's root directory in your terminal and execute the following commands:

pipenv install
pipenv shell
pipenv run python assignment0/main.py --incidents <url>
Here, URL refers to the URL of the PDF.

To execute the test cases, run the following command from the project's root directory:
pipenv run python -m pytest

GIF

## Functions Description
fetchincidents(url): Downloads a PDF from the given URL and saves it locally for processing. It returns the path to the saved PDF file.

Where the file is stored: The file is stored in the '/tmp' directory. This is a common practice that works across Unix-based platforms like Linux and macOS.
Storing the file in the tmp directory helps isolate it from the rest of the system files and user data, making it a desirable factor from a security perspective. This is important since we are downloading a file from a link on the Internet. Furthermore, the tmp directory is designed for storing temporary files only needed during the execution of a program. The PDF is not required after the program runs, so the OS can clear the file the next time it clears the '/tmp' directory. This project is intended to work with and developed using Linux, so the '/tmp' folder has been used. For Windows, a user-specific temp folder would be used.
extract_incidents_from_pdf(pdf_path): Opens the downloaded PDF file and extracts incidents data based on predefined coordinates. It returns a list of dictionaries, each representing an incident.

createdb(): Initializes a SQLite database to store incident data. If the database already exists, it is replaced with a new one.

populatedb(db, incidents): Takes the database connection object and the list of extracted incidents, then populates the database with these incidents.

status(db): Queries the populated database to count the occurrences of each type of incident and prints the counts to standard output.

## Database Development
SQLite database has been used in this project. SQLite is a lightweight, file-based database management system that is embedded into the end program. It has been used in this project due to the simplicity, efficiency, and reliability it offers.

The database contains a single table with the following schema:

incident_time: Stores the date and time when the incident occurred. The data type is TEXT, formatted to ensure consistency in date-time representation.
incident_number: A unique identifier for each incident report. This field is crucial for ensuring that each entry in the database represents a distinct incident.
incident_location: Describes the location where the incident occurred.
nature: Specifies the nature or type of the incident, providing a brief description or categorization of the incident.
incident_ori: Stands for the Originating Agency Identifier, which is a code that identifies the reporting agency.
All the columns above are of data type TEXT.

Database Operations: The application includes functions for creating the database (createdb), inserting new incident data (populatedb), and querying the database to report on the nature and count of incidents (status). These operations are essential for the application's functionality, allowing it to store, update, and analyze incident data efficiently.

## Bugs and Assumptions:
No known bugs for the desired output. However, there are a couple of assumptions listed below.
It is assumed that the layout of the PDF remains the same. Changes to the layout, such as switching of columns, will require a revision of the coordinates listed. This is a layout-dependent solution which does not use any regular expressions. This methodology has been decided upon for the most accurate output.
This solution is built for data extraction of the Norman PD Incident Reports. It is not transferrable to other PDFs without revision of the code.