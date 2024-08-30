import pandas as pd
import validations as val
import json

predicted_yields_path = './data/yield_predictions_2024.csv'
predicted_yields = pd.read_csv(predicted_yields_path)

print(predicted_yields.head())
print("********* Farmer Credit System ********")

UIcontext_path = './UIcontext/context.json'
with open(UIcontext_path) as f:
    context = json.load(f)

crop = context['crop']
season = context['season']
crop_area = context['crop_area']

#eventually take from farmer data
district = context['district']

#check if district is valid
if district not in predicted_yields['district'].unique():
    print("Invalid district")
    exit()

#check if crop name is valid
if crop not in predicted_yields['crop'].unique():
    print("Invalid crop name")
    exit()

# check if crop area is valid
# if not val.validate_area(crop_area):
#     print("Invalid crop area")
#     print("Not elegible for kissan loan")
#     exit()

#check if season is valid
if season not in predicted_yields['season'].unique():
    print("Invalid season")
    exit()

# validate if crop is grown in the selected season & selected district
if not val.validate_crop(crop, season, district):
    print("Crop is not grown in the selected season & district")
    print("Not elegible for kissan loan")
    exit()

# do a check on if yield of crop is decreasing over the years
# if yield is decreasing, then do not give loan
# if not val.yield_decreasing(crop_name):
#     print("Yield of the crop is decreasing over the years")
#     print("Not elegible for kissan loan")
#     exit()

# filter the data based on the inputs
filtered_data = predicted_yields[(predicted_yields['crop'] == crop) & (predicted_yields['season'] == season) & (predicted_yields['district'] == district)]

#display the filtered data
print(filtered_data)

#give yield prediction
yield_prediction = filtered_data['yield'].values[0] 
print("Predicted yield for year 2024: ", yield_prediction, " tonnes/hectares")

predicted_yield = filtered_data['yield'].values[0] * crop_area
print("Predicted yield for the farmer: ", predicted_yield, " tonnes")
