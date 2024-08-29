import pandas as pd

def validate_area(crop_area):
    try:
        crop_area = float(crop_area)
        if crop_area <= 0:
            print("Invalid crop area")
            return False
        # if crop area is greater than the land area the farmer has
        # if crop_area > farmer_data['land_area'].values[0]:
        #     print("Crop area is greater than the land area the farmer has")
        #     return False
        return True
    except ValueError:
        print("Invalid crop area")
        return False
    
def validate_crop(crop_name, season, district, yield_df ):
    # check if the crop is grown in the selected season & selected district
    if len(yield_df[(yield_df['crop'] == crop_name) & (yield_df['season'] == season) & (yield_df['district'] == district)]) == 0:
        return False
    return True

def yield_decreasing(crop_name):
    return True
    # check if yield of crop is decreasing over the years