import matplotlib.pyplot as plt
import matplotlib.animation as animation
import json
from datetime import datetime

# Initialize lists for future CPU usage data and time
future_cpu_usage = []
list_future_time = []

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(10, 6))
line, = ax.plot(list_future_time, future_cpu_usage, label="CPU Usage", marker='o', color='b', linestyle='-')

# Add static horizontal lines at 25%, 50%, and 100% CPU usage limits
ax.axhline(y=25, color='r', linestyle='--', label="Limit: 25%")
ax.axhline(y=50, color='orange', linestyle='--', label="Limit: 50%")
ax.axhline(y=100, color='purple', linestyle='--', label="Limit: 100%")

ax.set_xlabel("Time")
ax.set_ylabel("CPU Usage (%)")
ax.set_title("Real-Time CPU Usage with Limits")
ax.legend()
ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%H:%M:%S"))
plt.xticks(rotation=45)
plt.tight_layout()


# Function to read and parse data from file
def getdata():
    # Clear existing data for each update
    future_cpu_usage.clear()
    list_future_time.clear()
    
    # Read the data from the file
    with open("prediction.json", "r") as file:
        for line in file:
            data = json.loads(line.strip())
            
            # Convert time string to datetime object for plotting
            time_obj = datetime.strptime(data["time"], "%Y-%m-%d %H:%M:%S")
            list_future_time.append(time_obj)
            future_cpu_usage.append(data["cpu"])


# Function to update the plot
def update(frame): 
    getdata()
    
    # Update the line with new data
    line.set_ydata(future_cpu_usage)
    line.set_xdata(list_future_time)
    
    # Adjust plot limits
    ax.relim()
    ax.autoscale_view()
    return line,


# Set up the animation
ani = animation.FuncAnimation(fig, update, interval=60000)  # Update every 1000 milliseconds (1 second)

plt.show()


