import pandas as pd

predicted_yields_path = './data/Yield_data.csv'
predicted_yields = pd.read_csv(predicted_yields_path)

past_yield_path = './pastData/pastYields.csv'
past_yield = pd.read_csv(past_yield_path)
    
def validate_crop(crop_name, season, district):
    # check if the crop is grown in the selected season & selected district
    if len(predicted_yields[(predicted_yields['crop'] == crop_name) & (predicted_yields['season'] == season) & (predicted_yields['district'] == district)]) == 0:
        return False
    return True

def validate_area(crop_area, farmer_area):
        try:
            if crop_area <= 0:
                print("Invalid crop area")
                return False
            #if crop area is greater than the land area the farmer has
            if crop_area > farmer_area:
                print("Crop area is greater than the land area the farmer has")
                return False
            return True
        except ValueError:
            print("Invalid crop area")
            return False
        
def validate_district(district):
    # check if the district is valid
    if district not in predicted_yields['district'].unique():
        print("Invalid district")
        return False
    return True
        
def yield_decreasing(crop, district):
    return False
    # check if yield of crop is decreasing over the years