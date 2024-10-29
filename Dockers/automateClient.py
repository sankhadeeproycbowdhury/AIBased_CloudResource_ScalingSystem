import time
import random
import socket

# Server setup
hostname = socket.gethostname()  
HOST = socket.gethostbyname(hostname) # Localhost or replace with server IP

def runClient():
    PORT = 65432 # Port to listen on
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"connected Successfully")
    

def randomly_run_program(duration):
    """Runs a program at random intervals for a given duration."""
    end_time = time.time() + duration  # Calculate the end time
    while time.time() < end_time:
        interval = random.randint(1, 10)
        time.sleep(interval)  # Wait for the random interval
        runClient()  # Run the program

if __name__ == "__main__":
    # Duration to run the random execution (in seconds)
    execution_duration = 60  # Run for 30 seconds

    randomly_run_program(execution_duration)
