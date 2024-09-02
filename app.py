import pandas as pd
import src.validations as val
import json
import src.loan_amount_calculator as lac
import src.helper as helper

predicted_yields_path = 'data/predictedYields.csv'
predicted_yields = pd.read_csv(predicted_yields_path)

print("********* Farmer Credit System ********")

UIcontext_path = './UIcontext/context.json'
with open(UIcontext_path) as f:
    context = json.load(f)

crop = context['crop']
season = context['season']
crop_area = context['crop_area']
land_type = context['land_type']

#eventually take from farmer data
district = context['district']

#check if district is valid
if val.validate_district(district)!=True:
    print("Invalid crop name")
    exit()

#check if crop area is valid
if val.validate_area(crop_area)!=True:
    print("Invalid crop area")
    exit()

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
if val.yield_decreasing(crop, district):
    print("Yield of the crop is decreasing over the years")
    print("Not elegible for kissan loan")
    exit()

# filter the data based on the inputs
filtered_data = predicted_yields[(predicted_yields['crop'] == crop) & (predicted_yields['season'] == season) & (predicted_yields['district'] == district)]

#display the filtered data
print(filtered_data)

#give yield prediction
yield_prediction = filtered_data['yield'].values[0] 
print("Predicted yield for year 2024: ", yield_prediction, " tonnes/hectares")

predicted_yield = filtered_data['yield'].values[0] * crop_area
print("Predicted yield for the farmer: ", predicted_yield, " tonnes")


# Get SOF for crop
SOF_path = 'data/SOF.csv'
sof_df = pd.read_csv(SOF_path)

# get SOF as crop, irrigation type & SOF
crop_cost = helper.get_sof_of_crop(sof_df, crop, land_type)

#calculate the kisaan loan amount
kisaan_loan_amount = lac.calcKisaanLoan(predicted_yield, crop_cost)
print("Kissan loan amount: ", kisaan_loan_amount)

# get APMC price for the crop
APMC_path = 'data/APMC.csv'
apmc_df = pd.read_csv(APMC_path)

# get APMC price for the crop
crop_price = helper.get_apmc_price(apmc_df, crop, district)




