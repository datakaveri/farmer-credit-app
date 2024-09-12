import pandas as pd
import src.validations as val
import json
import src.loan_amount_calculator as lac
import src.helper as helper
import src.data_preprocessing as preProcessor
from datetime import datetime

print("********* Farmer Credit System ********")

kisaan_loan_amount = 0
consumer_loan_amount = 0
status = ""
status_code = "000"

while True:
    print("Pre-processing data...")
    preProcessor.modifySOFData()
    print("Data pre-processing complete")

    # Load the data
    predicted_yields_path = 'data/Yield_data.csv'
    predicted_yields = pd.read_csv(predicted_yields_path)

    farmer_data_path = 'data/farmer_data.json'
    with open(farmer_data_path) as f:
        farmer_data = json.load(f)

    UIcontext_path = './UIcontext/context.json'
    with open(UIcontext_path) as f:
        context = json.load(f)

    crop = context['crop']
    season = context['season']
    crop_area = context['crop_area']
    land_type = context['land_type']

    #take district from farmer data
    if 'results' in farmer_data and isinstance(farmer_data['results'], list) and farmer_data['results']:
        # Sort the results by observationDateTime in descending order
        sorted_results = sorted(
            farmer_data['results'], 
            key=lambda x: datetime.strptime(x['observationDateTime'], "%Y-%m-%dT%H:%M:%S%z"), 
            reverse=True
        )

        # Get the latest record (first item in the sorted list)
        latest_record = sorted_results[0]

        print(latest_record)
        
        # Get the districtName and landExtent from the latest record
        district = latest_record.get('districtName')
        farmer_area = latest_record.get('landExtent')

        # Convert farmer area to hectares & round off to 2 decimal places
        farmer_area = round(farmer_area * 0.404686, 2)
        print(f"Farmer Land Area: {farmer_area} hectares")
        print(f"District Name: {district}")

        district = district.title()
        # if district is Narayanpet, change it to Narayanapet
        if district == 'Narayanpet':
            district = 'Narayanapet'
    else:
        print("No results found or 'results' is not a list.")
        status = "Farmer data not available"
        status_code = "401"
        break

    #check if district is valid
    if val.validate_district(district)!=True:
        print("Yield information not available for farmer district")
        status = "Yield information not available for farmer district"
        status_code = "402"
        break

    #check if crop area is valid
    if val.validate_area(crop_area, farmer_area)==-1:
        print("Invalid crop area, has to be a positive number")
        status = "Invalid crop area, enter positive number"
        status_code = "403"
        break

    if val.validate_area(crop_area, farmer_area)==0:
        status = f"Invalid crop area, crop area greater than land area owned by farmer ({farmer_area} hectares)."
        status_code = "403"
        break

    #check if season is valid
    if season not in predicted_yields['season'].unique():
        print("Invalid season")
        status = "Invalid season"
        status_code = "404"
        break

    # validate if crop is grown in the selected season & selected district
    if not val.validate_crop(crop, season, district):
        print("Crop is not grown in the selected season & district")
        print("Not elegible for kissan loan")
        status = "Crop is not grown in the selected season & district, not eligible for kisaan loan"
        status_code = "405"
        break

    # do a check on if yield of crop is decreasing over the years
    # if yield is decreasing, then do not give loan
    if val.yield_decreasing(crop, district):
        print("Yield of the crop is decreasing over the years")
        print("Not elegible for kisaan loan")
        status = "Yield of the crop is decreasing over the years, not eligible for kissan loan"
        status_code = "406"
        break

    # filter the data based on the inputs & check if data is available
    filtered_data = predicted_yields[(predicted_yields['crop']==crop) & (predicted_yields['district']==district) & (predicted_yields['season']==season)]

    #display the filtered data
    print(filtered_data)

    #give yield prediction
    yield_prediction = filtered_data['yield'].values[0] 
    print("Predicted yield for year 2024: ", yield_prediction, " tonnes/hectares")

    predicted_yield = filtered_data['yield'].values[0] * crop_area
    print("Predicted yield for the farmer: ", predicted_yield, " tonnes")


    # Get SOF for crop
    SOF_path = 'data/SOF_data.csv'
    sof_df = pd.read_csv(SOF_path)

    # get SOF as crop, irrigation type & SOF
    crop_sof = helper.get_sof_of_crop(sof_df, crop, land_type)
    if crop_sof == 0:
        print("Scale of Finance is not available for the selected crop &/or land type")
        print("Not elegible for kisaan loan")
        status = "Scale of Finance is not available for the selected crop &/or land type"
        status_code = "408"
        break
    print("Scale of Finance: ", crop_sof, " Rs per acre")

    #calculate the kisaan loan amount
    total_crop_cost = lac.calcKisaanLoan(crop_area, crop_sof)
    kisaan_loan_amount = total_crop_cost
    print("Kissan loan amount: Rs. ", kisaan_loan_amount)

    # get APMC price for the crop
    APMC_path = 'data/APMC_data.csv'
    apmc_df = pd.read_csv(APMC_path)

    # get APMC price for the crop
    crop_price = helper.get_apmc_price(apmc_df, crop, district, season)
    if crop_price == 0:
        print("Crop price is not available for the selected season &/or district")
        print("Not elegible for consumer loan")
        status = "Not elegible for consumer loan, crop APMC price is not available for the selected season &/or district"
        status_code = "301"
        break
    else:
        consumer_loan_amount = lac.calcConsumerLoan(predicted_yield, total_crop_cost, crop_price)
        if consumer_loan_amount == 0:
            print("Crop cost is greater than the selling price, no profit made")
            print("Not elegible for consumer loan")
            status = "Not elegible for consumer loan, no estimated profit made"
            status_code = "302"
            break
        else:
            print("Consumer loan amount: Rs. ", consumer_loan_amount)
            status = "Consumer and Kisaan loan amounts calculated successfully"
            status_code = "200"
            break


response = {
    "output": {
        "kisaan_loan_amount": kisaan_loan_amount,
        "consumer_loan_amount": consumer_loan_amount
    },
    "status": status,
    "status_code": status_code
}

with open("outputFolder/output.json", "w") as f:
    json.dump(response, f)
print("Output written to output.json")

print("********* Farmer Credit System EXIT ********")


