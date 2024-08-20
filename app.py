import pandas as pd

predicted_yields_path = 'yield_predictions_2024.csv'
predicted_yields = pd.read_csv(predicted_yields_path)

print(predicted_yields.head())

print("********* Yield Prediction System ********")

#take input from user
print("Districts available: ", predicted_yields['district'].unique())
district = input("Enter farmer district: ")

#check if district is valid
if district not in predicted_yields['district'].unique():
    print("Invalid district")
    exit()

print("Crops available: ", predicted_yields['crop'].unique())
crop_name = input("Enter the crop name: ")

#check if crop name is valid
if crop_name not in predicted_yields['crop'].unique():
    print("Invalid crop name")
    exit()

print("Seasons available: ", predicted_yields['season'].unique())
season = input("Enter the season (K for Khareef, R for Rabi, WY for Whole Year): ")

#check if season is valid
if season not in predicted_yields['season'].unique():
    print("Invalid season")
    exit()

#filter the data based on user input
filtered_data = predicted_yields[(predicted_yields['crop'] == crop_name) & (predicted_yields['season'] == season) & (predicted_yields['district'] == district)]
#check if data is available for the selected options
if filtered_data.empty:
    print("Data not available for the selected options")
    exit()

#display the filtered data
print(filtered_data)

#give yield prediction
print("Predicted yield for year 2024: ", filtered_data['yield'].values[0])

#take input land area (in hectares)
land_area = float(input("Enter land area on which crop is to be grown (in hectares): "))
#calculate the predicted yield in tonnes
predicted_yield = filtered_data['yield'].values[0] * land_area
print("Predicted yield for year 2024 for ", land_area, " hectares: ", predicted_yield, " tonnes")

#get the price of the crop from price data (district, crop)