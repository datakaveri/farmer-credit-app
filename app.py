import pandas as pd
import src.validations as val
import json
import src.loan_amount_calculator as lac
import src.helper as helper
import src.data_preprocessing as preProcessor

def main():
    print("********* Farmer Credit System ********")

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
        # Get the districtName from the first item
        district = farmer_data['results'][0].get('districtName')

        farmer_area = farmer_data['results'][0].get('landExtent') 
        # convert farmer area to hectares & round off to 2 decimal places
        farmer_area = round(farmer_area * 0.404686, 2)
        print(f"Farmer Land Area: {farmer_area} hectares")
        print(f"District Name: {district}")
    else:
        print("No results found or 'results' is not a list.")

    # convert district to first letter capital
    district = district.title()

    # if district is Narayanpet, change it to Narayanapet
    if district == 'Narayanpet':
        district = 'Narayanapet'


    #check if district is valid
    if val.validate_district(district)!=True:
        print("District information not available")
        with open("output/output.json", "w") as f:
            json.dump({"status_code": "907", "status": "District information not available"}, f)
            return 0, 0

    #check if crop area is valid
    if val.validate_area(crop_area, farmer_area)!=True:
        print("Invalid crop area")
        with open("output/output.json", "w") as f:
            json.dump({"status_code": "908", "status": "Invalid crop area"}, f)
            return 0, 0

    #check if season is valid
    if season not in predicted_yields['season'].unique():
        print("Invalid season")
        with open("output/output.json", "w") as f:
            json.dump({"status_code": "909", "status": "Invalid season"}, f)
            return 0, 0

    # validate if crop is grown in the selected season & selected district
    if not val.validate_crop(crop, season, district):
        print("Crop is not grown in the selected season & district")
        print("Not elegible for kissan loan")
        with open("output/output.json", "w") as f:
            json.dump({"status_code": "910", "status": "Crop is not grown in the selected season & district"}, f)
            return 0, 0

    # do a check on if yield of crop is decreasing over the years
    # if yield is decreasing, then do not give loan
    if val.yield_decreasing(crop, district):
        print("Yield of the crop is decreasing over the years")
        print("Not elegible for kissan loan")
        with open("output/output.json", "w") as f:
            json.dump({"status_code": "911", "status": "Yield of the crop is decreasing over the years"}, f)
            return 0, 0

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
    SOF_path = 'data/SOF_data.csv'
    sof_df = pd.read_csv(SOF_path)

    # get SOF as crop, irrigation type & SOF
    crop_sof = helper.get_sof_of_crop(sof_df, crop, land_type)
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
        consumer_loan_amount = 0
    else:
        consumer_loan_amount = lac.calcConsumerLoan(predicted_yield, total_crop_cost, crop_price)
    print("Consumer loan amount: Rs. ", consumer_loan_amount)

    print("********* Farmer Credit System EXIT ********")
    return kisaan_loan_amount, consumer_loan_amount


if __name__ == "__main__":
    main()


