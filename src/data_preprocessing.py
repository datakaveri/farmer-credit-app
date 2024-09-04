import pandas as pd 
import csv

def modifyPredictedYieldsData():
    predicted_yields_path = 'data/predictedYields.csv'
    predicted_yields = pd.read_csv(predicted_yields_path)

    predicted_yields['year'] = pd.to_datetime(predicted_yields['year']).dt.year
    predicted_yields_filtered = predicted_yields[predicted_yields['year'] != 2023]

    # Save the filtered data back to the CSV file (or a new file)
    predicted_yields_filtered.to_csv('data/predictedYields.csv', index=False)

    print("Filtered data saved")

def modifySOFData():
    sof_data_path = 'data/SOF_data.csv'
    with open(sof_data_path, 'r') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader) 

    for row in rows:
        crop = row['Crop']
        landType =''

        if '(' in crop and ')' in crop:
        # Extract the part inside brackets
            bracket_content = crop[crop.find('(') + 1 : crop.find(')')]
            
            # Check if it's 'UI' or 'Irr.'
            if bracket_content in ['UI', 'Irr.']:
                landType = bracket_content.rstrip('.')  # Remove the dot from 'Irr.'

            # Remove the part inside brackets from 'Crop'
            row['Crop'] = crop[:crop.find('(')].strip()

        # Add the LandType to the row
        row['LandType'] = landType

    fieldnames = ['Crop', 'LandType', 'maxSOF']

    with open('data/SOF_data.csv', 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        # Write the header
        writer.writeheader()
        
        # Write the rows
        writer.writerows(rows)

    print("Modified SOF data saved")

def modifyAPMCData():
    predictedPrices_path = 'data/predictedPrices.csv'
    predictedPrices = pd.read_csv(predictedPrices_path)

    predictedPrices['year'] = pd.to_datetime(predictedPrices['year']).dt.year
    predictedPrices_filtered = predictedPrices[predictedPrices['year'] != 2026]

    # Save the filtered data back to the CSV file (or a new file)
    predictedPrices_filtered.to_csv('../data/predictedPrices.csv', index=False)

    print("Filtered APMC data saved")
