import pandas as pd 

def modifyPredictedYieldsData():
    predicted_yields_path = 'data/predictedYields.csv'
    predicted_yields = pd.read_csv(predicted_yields_path)

    predicted_yields['year'] = pd.to_datetime(predicted_yields['year']).dt.year
    predicted_yields_filtered = predicted_yields[predicted_yields['year'] != 2023]

    # Save the filtered data back to the CSV file (or a new file)
    predicted_yields_filtered.to_csv('data/predictedYields.csv', index=False)

    print("Filtered data saved")

def modifySOFData():
    sof_data_path = 'data/SOF-TS.csv'
    sof_data = pd.read_csv(sof_data_path)

    sof_data = sof_data.drop(columns=['SI. No.', 'Scale of Finance (2023-24)'])

    # Save the modified data back to the CSV file (or a new file)
    sof_data.to_csv('../data/SOF-TS.csv', index=False)

    print("Modified SOF data saved")

def modifyAPMCData():
    predictedPrices_path = 'data/predictedPrices.csv'
    predictedPrices = pd.read_csv(predictedPrices_path)

    predictedPrices['year'] = pd.to_datetime(predictedPrices['year']).dt.year
    predictedPrices_filtered = predictedPrices[predictedPrices['year'] != 2026]

    # Save the filtered data back to the CSV file (or a new file)
    predictedPrices_filtered.to_csv('../data/predictedPrices.csv', index=False)

    print("Filtered APMC data saved")
