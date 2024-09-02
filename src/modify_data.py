import pandas as pd 
import random

def modifyPredictedYieldsData():
    predicted_yields_path = '../data/predictedYields.csv'
    predicted_yields = pd.read_csv(predicted_yields_path)

    predicted_yields_filtered['year'] = pd.to_datetime(predicted_yields_filtered['year']).dt.year
    predicted_yields_filtered = predicted_yields[predicted_yields['year'] != 2023]

    # Save the filtered data back to the CSV file (or a new file)
    predicted_yields_filtered.to_csv('data/predictedYields.csv', index=False)

    print("Filtered data saved")

def modifySOFData():
    sof_data_path = '../data/SOF-TS.csv'
    sof_data = pd.read_csv(sof_data_path)

    sof_data = sof_data.drop(columns=['SI. No.', 'Scale of Finance (2023-24)'])

    # sof_data['Scale of Finance (2024-25) '] = sof_data['Scale of Finance (2024-25) '].apply(pick_random_from_range)

    # Save the modified data back to the CSV file (or a new file)
    sof_data.to_csv('../data/SOF-TS.csv', index=False)

    print("Modified SOF data saved")

def modifyAPMCData():
    predictedPrices_path = '../data/predictedPrices.csv'
    predictedPrices = pd.read_csv(predictedPrices_path)

    

# Function to pick a random value from the range
def pick_random_from_range(range_str):
    min_val, max_val = map(int, range_str.split('-'))
    return random.randint(min_val, max_val)