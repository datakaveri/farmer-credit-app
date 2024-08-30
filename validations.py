import pandas as pd

# load the data
predicted_yields_path = './data/yield_predictions_2024.csv'
# farmer_data_path = 'farmer_data.csv'

predicted_yields = pd.read_csv(predicted_yields_path)
# farmer_data = pd.read_csv(farmer_data_path)

# def validate_area(crop_area):
#     try:
#         crop_area = float(crop_area)
#         if crop_area <= 0:
#             print("Invalid crop area")
#             return False
#         # if crop area is greater than the land area the farmer has
#         if crop_area > farmer_data['land_area'].values[0]:
#             print("Crop area is greater than the land area the farmer has")
#             return False
#         return True
#     except ValueError:
#         print("Invalid crop area")
#         return False
    
def validate_crop(crop_name, season, district):
    # check if the crop is grown in the selected season & selected district
    if len(predicted_yields[(predicted_yields['crop'] == crop_name) & (predicted_yields['season'] == season) & (predicted_yields['district'] == district)]) == 0:
        return False
    return True

#def yield_decreasing(yield_data, crop_name):
    # check if yield of crop is decreasing over the years