# Convert sqlite to csv

import csv
import sqlite3
import os

filename = input('Enter the name of the sqlite db file: ')
filename_csv = filename.split('.')[0] + '.csv'

# make "formatted_data" and "parsed_data" directories if they don't exist
if not os.path.exists("formatted_data"):
    os.makedirs("formatted_data")

if not os.path.exists("parsed_data"):
    os.makedirs("parsed_data")

def sqlite_to_csv(filename, filename_csv):

    # Connect to the database
    conn = sqlite3.connect(filename)
    c = conn.cursor()

    # parse through the database and create an array of the tables
    tables = []
    for row in c.execute("SELECT name FROM sqlite_master WHERE type='table';"):
        tables.append(row[0])

    # Print the tables
    print('Tables in the database:')
    for table in tables:
        print(table)

    # Create a new csv file
    with open(filename_csv, 'w') as f:
        writer = csv.writer(f)
        # writer.writerow(['id', 'time', 'data'])
        # for row in c.execute('SELECT * FROM data'):
        #     writer.writerow(row)

        # for each table in the database, write the table to the csv file, separate each table with a row of dashes
        for table in tables:
            writer.writerow([table])
            for row in c.execute('SELECT * FROM ' + table):
                writer.writerow(row)
            writer.writerow(['-' * 50])

    # Close the csv file
    f.close()

    # Close the connection
    conn.close()

    return filename_csv

# split sections of the unparsed csv to their own individual csv files
def parse_csv(filename_csv, array_of_table_names):

    # open the csv file
    with open(filename_csv, 'r') as f1:
        reader = csv.reader(f1)
        data = list(reader)

    # go through the data and split the csv into individual csv files based on the tables in
    # array_of_table_names
    
    # For each of the tables in the array
    for table in array_of_table_names:
        # Create a new csv file
        with open("parsed_data/" + table + '.csv', 'w') as f2:
            
            # find the line number of the table name by finding a matching string
            table_line = 0
            for i in range(len(data)):
                if data[i][0] == table:

                    # make sure there is nothing else on the same line as the table name
                    if len(data[i]) == 1:
                        table_line = i
                        break
            
            
            print("For table: "+ table +", table located at: " + str(table_line))

            # write the lines below the table name to the new csv file until a line of dashes is found
            for i in range(table_line + 1, len(data)):
                if data[i][0] == '-' * 50:
                    break
                else:
                    writer = csv.writer(f2)
                    writer.writerow(data[i])

        # Close the csv file
        f1.close()

    # Close the csv file
    f2.close()

# format the csv files in the "parsed_data" directory
def format_csv(input_file, time_index, data_index, plant_name, time_unit, data_unit):

    # open the csv file specified in parsed_data
    with open("parsed_data/" + input_file, 'r') as f1:
        reader = csv.reader(f1)
        data = list(reader)

    # create a new csv file in formatted_data with the plant name
    with open("formatted_data/" + plant_name + '.csv', 'w') as f2:

        # The column index specified in time index is written to the first column of the new csv file
        # The column index specified in data index is written to the second column of the new csv file
        # The plant name is written to the third column of the new csv file
        # set the header names to time_unit, data_unit, and plant_name
        writer = csv.writer(f2)
        writer.writerow([time_unit, data_unit, plant_name])

        # write the time and data to the new csv file
        for i in range(len(data)):
            writer.writerow([data[i][time_index], data[i][data_index], plant_name])

    # Close the csv file
    f1.close()

    # Close the csv file
    f2.close()

# Format the time column to be in the format of H/MIN/S with a max of 2 decimal places
def format_time(csv_file):
    with open("formatted_data/" + csv_file, 'r') as f1:
        reader = csv.reader(f1)
        data = list(reader)

    with open("formatted_data/" + csv_file, 'w') as f2:
        writer = csv.writer(f2)
        # writer.writerow(['Time', 'Data', 'Plant'])
        for i in range(len(data)):
            time = data[i][0]

            # if not the top row
            if i != 0:
                time = time.split(':')

                # remove any characters beyond the 6th character
                time[2] = time[2][:6]
                # reformat the time to be in the format of H:MIN:S 
                time = time[0] + ":" + time[1] + ":" + time[2].split('.')[0]

            writer.writerow([time, data[i][1], data[i][2]])

    f1.close()
    f2.close()


        
    


# Run the functions
sqlite_to_csv(filename, filename_csv)
tables = ["air_readings", "air_readings_detailed", "new_air_readings"]
parse_csv(filename_csv, tables)

# test format csv on air_readings_detailed.csv
format_csv("air_readings_detailed.csv", 2, 3, "Air_Temperature", "H/MIN/S", "Degrees C")

format_time("Air_Temperature.csv")


