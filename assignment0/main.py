import argparse
import urllib.request
import os
import sqlite3
import fitz

def fetchincidents(url):
    """
    Download the PDF from the given URL and return the file path.
    """
    response = urllib.request.urlopen(url)
    file_name = os.path.join('/tmp', 'incident.pdf')
    with open(file_name, 'wb') as file:
        file.write(response.read())
    return file_name


def extract_incidents_from_pdf(pdf_path):

    colStartCoordinates = [52.560001373291016,150.86000061035156,229.82000732421875,423.19000244140625,623.8599853515625]
    columnWise_data = ["","","","",""]
  

    pdf_document = fitz.open(pdf_path)
    incidents = []
    i = 0
    for page in pdf_document:
        previousLineId = 0 #A line can be date+time, address, etc
        previousBlockId = 1
        words = page.get_text("words")
        if i == 0:
            words = words[9:-7]
            i+=1
        if i == len(pdf_document) - 1:
            words = words[:-2]
        #This is done to append a word to the end of the list of words. 
        #If this isn't done, the last word of each page would be missing, since I always operate on the subsequent word in this code.
        words = words +[words[0]]

        
        line = ""
        x = 0
        #(0:x0, 1:y0, 2:x1, 3:y1, 4:"word", 5:block_no, 6:line_no, 7:word_no)
        for word in words:
            if previousLineId == word[6]:
                if word[7] == 0:
                    line = word[4]
                    x = word[0]
                else:
                    line = line + " " + word[4] 
            
            else:
                for index,colstartCoordinate in enumerate(colStartCoordinates):
                    if index < len(colStartCoordinates)-1:
                        if x < colStartCoordinates[index+1] and x >= colStartCoordinates[index]:
                            handle_multiple_lines(columnWise_data,index,line)
                            
                    if index == len(colStartCoordinates)-1 and x >= colStartCoordinates[index]:
                            handle_multiple_lines(columnWise_data,index,line)
                line = word[4]
                x = word[0]
                previousLineId = word[6]

            if word[5] != previousBlockId:
                incident = {
                         "date_time": columnWise_data[0],
                         "incident_number": columnWise_data[1],
                         "location": columnWise_data[2],
                         "nature": columnWise_data[3],
                         "incident_ori": columnWise_data[4]
                     }
                columnWise_data = ["","","","",""]
                incidents.append(incident)
                previousBlockId = word[5]
   
    pdf_document.close()
    return incidents

def handle_multiple_lines(columnWise_data,index,line):
    if columnWise_data[index]:
        columnWise_data[index] = columnWise_data[index] + " " + line
    else:
        columnWise_data[index] = line


def createdb():
    """
    Create a SQLite database and return the connection object.
    """
    db_file = 'resources/normanpd.db'
    # Check if the database file already exists, and if it does, delete it
    if os.path.exists(db_file):
        os.remove(db_file)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS incidents (
                        incident_time TEXT,
                        incident_number TEXT,
                        incident_location TEXT,
                        nature TEXT,
                        incident_ori TEXT
                      );''')
    conn.commit()
    return conn

def populatedb(db, incidents):
    """
    Insert incident data into the database.
    """
    cursor = db.cursor()
    # Convert each incident dictionary to a tuple in the correct order
    incident_tuples = [
        (incident["date_time"], incident["incident_number"], incident["location"], incident["nature"], incident["incident_ori"])
        for incident in incidents
        if any(incident.values())
    ]
    cursor.executemany('''INSERT INTO incidents 
                          (incident_time, incident_number, incident_location, nature, incident_ori) 
                          VALUES (?, ?, ?, ?, ?);''', incident_tuples)
    db.commit()


def status(db):
    """
    Print the nature of incidents and their count.
    """
    cursor = db.cursor()
    cursor.execute('''SELECT nature, COUNT(*) as count 
                      FROM incidents 
                      GROUP BY nature 
                      ORDER BY count DESC, nature;''')
    results = cursor.fetchall()
    blank_count = 0
    for nature, count in results:
        if nature:
            print(f"{nature}|{count}")
        else:
            blank_count += count
    if blank_count != 0:
        print(f"|{blank_count}")
    

def main(url):
    # Download data
    incident_data = fetchincidents(url)

    # Extract data
    incidents = extract_incidents_from_pdf(incident_data)
    
    # Create new database
    db = createdb()
    
    # Insert data
    populatedb(db, incidents)
    
    # Print incident counts
    status(db)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, 
                        help="Incident summary url.")
    
    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)
