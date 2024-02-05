import fitz  # PyMuPDF
import pytest
from assignment0 import main
import os
import sqlite3

def test_fetchincidents():
    url = "https://www.normanok.gov/sites/default/files/documents/2023-12/2023-12-18_daily_incident_summary.pdf"
    expected_path = "/tmp/incident.pdf"

    actual_path = main.fetchincidents(url)

    assert actual_path == expected_path
    assert os.path.exists(actual_path)
    assert os.path.getsize(actual_path) > 0

    os.remove(actual_path)

def test_exctract_incidents_from_pdf():
    url = "https://www.normanok.gov/sites/default/files/documents/2023-12/2023-12-18_daily_incident_summary.pdf"
    main.fetchincidents(url)
    pdf_path = "/tmp/incident.pdf"

    expected_incidents_subset = [
        {"date_time": "12/18/2023 2:46", "incident_number": "2023-00025192", "location": "", "nature": "", "incident_ori": "EMSSTAT"},
        {"date_time": "12/18/2023 8:49", "incident_number": "2023-00085150", "location": "201 REED AVE", "nature": "Disturbance/Domestic", "incident_ori": "OK0140200"},
    ]

    incidents = main.extract_incidents_from_pdf(pdf_path)

    for expected_incident in expected_incidents_subset:
        assert any(incident for incident in incidents if incident_matches(incident,expected_incident))
    
def incident_matches(incident, expected_incident):
    return (
        incident["date_time"] == expected_incident["date_time"] and
        incident["incident_number"] == expected_incident["incident_number"] and
        incident["location"] == expected_incident.get("location", incident["location"]) and
        incident["nature"] == expected_incident["nature"] and
        incident["incident_ori"] == expected_incident.get("incident_ori", incident["incident_ori"])
    )

def test_createdb():
    db_path = "resources/normanpd.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = main.createdb()
    assert os.path.exists(db_path)

    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name='incidents';")
    table_exists = cursor.fetchone()
    assert table_exists

    conn.close()
    os.remove(db_path)

def test_populatedb():
    conn = sqlite3.connect(":memory:")
    conn.execute('''CREATE TABLE IF NOT EXISTS incidents(
            incident_time TEXT,
            incident_number TEXT,
            incident_location TEXT,
            nature TEXT,
            incident_ori TEXT   
    );''')

    mock_incidents = [
        {"date_time": "12/18/2023 2:46", "incident_number": "2023-00025192", "location": "", "nature": "", "incident_ori": "EMSSTAT"},
        {"date_time": "12/18/2023 8:49", "incident_number": "2023-00085150", "location": "201 REED AVE", "nature": "Disturbance/Domestic", "incident_ori": "OK0140200"},
    ]

    main.populatedb(conn,mock_incidents)

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM incidents;")
    count = cursor.fetchone()[0]
    assert count == len(mock_incidents)

def test_status(capsys):
    conn = sqlite3.connect(":memory:")
    conn.execute('''CREATE TABLE IF NOT EXISTS incidents (
        incident_time TEXT,
        incident_number TEXT,
        incident_location TEXT,
        nature TEXT,
        incident_ori TEXT
    );''')
    conn.executemany('''INSERT INTO incidents 
                    (incident_time, incident_number, incident_location, nature, incident_ori) 
                    VALUES (?, ?, ?, ?, ?);''', 
                    [   ("01/01/2024 12:00", "1234-567890", "123 Example St", "Abdominal Pains/Problems", "ABC123"),
                        ("02/02/2024 13:30", "1235-567891", "124 Example St", "Cough", "ABC124"),
                        ("03/03/2024 14:40", "1236-567892", "125 Example St", "Sneeze", "ABC125"),
                        ("04/04/2024 15:50", "1237-567893", "126 Example St", "Breathing Problems", "ABC126"),
                        ("05/05/2024 16:00", "1238-567894", "127 Example St", "Noise Complaint", "ABC127"),
                        ("06/06/2024 17:10", "1239-567895", "128 Example St", "Cough", "ABC128"),
                        ("07/07/2024 18:20", "1240-567896", "129 Example St", "Sneeze", "ABC129"),
                    ])
    main.status(conn)

    captured = capsys.readouterr()

    expected_output = "Cough|2\nSneeze|2\nAbdominal Pains/Problems|1\nBreathing Problems|1\nNoise Complaint|1\n"

    assert captured.out == expected_output

    conn.close()




