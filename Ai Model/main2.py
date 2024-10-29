import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
import pickle
import psutil
import time
import subprocess
import json


class GRUModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(GRUModel, self).__init__()
        self.gru = nn.GRU(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        h_out, _ = self.gru(x)
        h_out = h_out[:, -1, :]  # Get the last time-step output
        out = self.fc(h_out)
        return out
    
    

# Load the Linear Regression model
with open('lr_model.pkl', 'rb') as file:
    lr_model = pickle.load(file)



# Instantiate the GRU model
input_size = 2
hidden_size = 100
output_size = 1
model = GRUModel(input_size, hidden_size, output_size)
model.load_state_dict(torch.load('model.pth'))
model.eval()




def scale_replicas(replica_count):
    try:
        # Construct the command to scale the deployment
        command = f"kubectl scale deployment/my-socket-server --replicas={replica_count}"
        command2 = f"kubectl get deployments"
        # Execute the command
        process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        process2 = subprocess.run(command2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        # Check for any errors
        if process.stderr:
            print(f"Error scaling deployment: {process.stderr}")
        else:
            print(f"Successfully scaled to {replica_count} replicas.")

        if process2.stderr:
            print(f"Error: {process2.stderr}")
        else:
            # Print the output of the `kubectl get pods` command
            print(f"Output:\n{process2.stdout}")

    except Exception as e:
        print(f"Error executing kubectl command: {str(e)}")
    
    

def predict_cpu_usage(raw_data, scaler_features, scaler_target, model, lr_model, time_step=10, future_steps=10):
    import torch
    import pandas as pd
    raw_data = pd.DataFrame(raw_data, columns=['CPU_Usage'])

    # Feature Engineering: Adding a moving average
    raw_data['Moving_Avg'] = raw_data['CPU_Usage'].rolling(window=time_step).mean().fillna(0)
    features = raw_data[['CPU_Usage', 'Moving_Avg']].values

    # Normalize data
    scaled_features = scaler_features.transform(features)

    # Prepare the last sequence for prediction
    last_sequence = scaled_features[-time_step:].reshape(1, time_step, 2)
    last_sequence = torch.tensor(last_sequence, dtype=torch.float32)

    # Predict the next future_steps values using the GRU model
    future_predictions = []
    for _ in range(future_steps):
        with torch.no_grad():
            pred = model(last_sequence).item()
            future_predictions.append(pred)
            # Update the sequence with the new prediction
            last_sequence = torch.roll(last_sequence, shifts=-1, dims=1)
            last_sequence[0, -1, 0] = pred
            moving_avg = torch.mean(last_sequence[0, :, 0]).item()
            last_sequence[0, -1, 1] = moving_avg

    # Convert future predictions to numpy array and inverse transform
    future_predictions = np.array(future_predictions).reshape(-1, 1)
    future_predictions_inv = scaler_target.inverse_transform(future_predictions)

    # Refine future predictions with Linear Regression
    future_predictions_lr = lr_model.predict(future_predictions_inv)

    return future_predictions_lr.flatten()




def Prediction(cpu_usage_df, model, lr_model):
    cpu_usage_df['Moving_Avg'] = cpu_usage_df['CPU_Usage'].rolling(window=10).mean().fillna(0)
    features = cpu_usage_df[['CPU_Usage', 'Moving_Avg']].values

    scaler_features = MinMaxScaler(feature_range=(0, 1))
    scaler_target = MinMaxScaler(feature_range=(0, 1))

    scaled_features = scaler_features.fit_transform(features)
    scaled_target = scaler_target.fit_transform(cpu_usage_df[['CPU_Usage']])
    time_step = 10
    raw_data = cpu_usage_df['CPU_Usage'].values[-time_step:].tolist()  # Use the last time_step values

    # Get predictions
    predicted_values = predict_cpu_usage(raw_data, scaler_features, scaler_target, model, lr_model, time_step=10, future_steps=10)
    # Get current time
    current_time = time.time()
    
    with open("prediction.json", "w") as file:   
        # Print the predicted values with future timestamps (per minute)
        for i, predicted_value in enumerate(predicted_values):
            future_time = current_time + (i + 1) * 60  # 1 minute apart (60 seconds)
            formatted_future_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(future_time))
            print(f'Predicted Time: {formatted_future_time}, Predicted CPU Usage: {predicted_value}%')
            output_data = {"time" : formatted_future_time, "cpu" : predicted_value}
            file.write(json.dumps(output_data) + "\n")
            if 25 < int(predicted_value) <= 50:
                scale_replicas(2)
            elif 50 < int(predicted_value) <= 100:
                scale_replicas(4)
            elif int(predicted_value) > 100:
                scale_replicas(8)
            else:
                print("Within Limit So, only 1 replica created")
                scale_replicas(1)
                
    
                    
# Run the loop every 1 minute (60 seconds)
prediction_duration = 10 * 60  # How long to keep predicting (in seconds) - adjust as needed
start_time = time.time()


while time.time() - start_time < prediction_duration:
    # Collect CPU usage data for 1 minute and print time with CPU usage
    cpu_usage_data = []
    print("Feeding Real Time Data....")
    for _ in range(60):
        cpu_usage = psutil.cpu_percent(interval=1)
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f'Time: {current_time}, CPU Usage: {cpu_usage}%')
        cpu_usage_data.append(cpu_usage)

    cpu_usage_df = pd.DataFrame(cpu_usage_data, columns=['CPU_Usage'])

    # Predict future CPU usage for the next 10 minutes
    Prediction(cpu_usage_df, model, lr_model)
    
    

     
