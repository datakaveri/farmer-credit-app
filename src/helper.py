
# Get SOF for crop
def get_sof_of_crop(sof_df, crop, land_type):
    sof = 0.0
    # check if land type is there for particular crop, if not return sof for crop irrespective of land type
    if len(sof_df[(sof_df['Crop']==crop) & (sof_df['LandType']==land_type)]) == 0:
        res = sof_df[sof_df['Crop']==crop]["maxSOF"]
    else: 
        res = sof_df[(sof_df['Crop']==crop) & (sof_df['LandType']==land_type)]["maxSOF"]
    # handle case when sof is not available
    # if sof is not available, return 0
    if len(res) == 0:
        return 0            
    sof = float(res.iloc[0]) 
    return sof

# get APMC price for the crop
def get_apmc_price(apmc_df, crop, district, season):
    price = 0.0
    # check if crop is grown in the selected season & selected district, if not return 0
    if len(apmc_df[(apmc_df['crop']==crop) & (apmc_df['district']==district) & (apmc_df['season']==season)]) == 0:
        return 0
    price = apmc_df[(apmc_df['crop']==crop) & (apmc_df['district']==district) & (apmc_df['season']==season)]['price'].to_list()[0]    
    price = float(price)
    return price


