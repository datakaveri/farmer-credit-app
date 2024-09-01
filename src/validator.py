import pandas as pd

class AppValidator:
    def __init__(self, crop_name, crop_area, season, district):
        self.crop_name = crop_name
        self.crop_area = float(crop_area)
        self.season = season
        self.district = district
    
    
    def validate_area(self):
        try:
            if self.crop_area <= 0:
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
        
    def validate_crop(self, yield_df ):
        # check if the crop is grown in the selected season & selected district
        if len(yield_df[(yield_df['crop'] == self.crop_name) & (yield_df['season'] == self.season) & (yield_df['district'] == self.district)]) == 0:
            return False
        return True

    def yield_decreasing(self):
        return True
        # check if yield of crop is decreasing over the year

    def validate(self, yield_df):
        valid_flag = self.validate_area() and self.validate_crop(yield_df) and self.yield_decreasing
        return valid_flag