import socket
import time
from datetime import datetime, timedelta
import threading
import sqlite3


# Server setup
hostname = socket.gethostname()  
HOST = socket.gethostbyname(hostname)  # Localhost or replace with server IP
PORT = 65432  # Port to listen on
table = 'server1'


# SQLite Database connection
database = sqlite3.connect('data.db', check_same_thread=False)
cursor = database.cursor()


# Variables to track requests
request_times = []  # To store the time when requests are received


cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS server1 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        start_time TEXT NOT NULL,
        end_time TEXT NOT NULL,
        request_count INTEGER NOT NULL
    );
'''
)

database.commit()

def insert_interval_to_db(start_time, end_time, request_count):
    """Insert interval and request count into the database."""
    cursor.execute(f'''INSERT INTO {table} (start_time, end_time, request_count) 
                      VALUES (?, ?, ?)''', (start_time.strftime("%Y-%m-%d %H:%M:%S"), 
                                            end_time.strftime("%Y-%m-%d %H:%M:%S"), 
                                            request_count))
    database.commit()


def plot_requests_per_interval(interval):
    """Function to plot the number of requests per time interval (e.g., seconds, minutes) and save to DB."""
    if not request_times:  # No requests have been logged yet
        print("No requests received yet. Waiting to plot.")
        return

    intervals = []
    request_count = []

    # Group requests by intervals
    start_time = request_times[0]
    end_time = datetime.now()
    current_interval_start = start_time
    
    while current_interval_start <= end_time:
        current_interval_end = current_interval_start + interval
        count = sum(current_interval_start <= t < current_interval_end for t in request_times)
        
        # Store interval and request count
        intervals.append(current_interval_start.strftime("%H:%M:%S"))
        request_count.append(count)
        
        # Insert interval and count into the database
        insert_interval_to_db(current_interval_start, current_interval_end, count)
        current_interval_start = current_interval_end


def plot_at_intervals(interval_seconds):
    """Function to plot the graph every N seconds."""
    while True:
        time.sleep(interval_seconds)  # Wait for the next interval
        print(f"Plotting requests every {interval_seconds} seconds.")
        plot_requests_per_interval(interval=timedelta(seconds=10))


# Start a separate thread for plotting at 60-second intervals
plot_thread = threading.Thread(target=plot_at_intervals, args=(60,))
plot_thread.daemon = True  # Daemon thread will exit when the main program exits
plot_thread.start()

# Start server to accept connections
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            
            # Log the time of request
            request_time = datetime.now()
            request_times.append(request_time)
            print(f"Request received at {request_time.strftime('%H:%M:%S')}")


# Close the database connection when the server exits
database.close()
