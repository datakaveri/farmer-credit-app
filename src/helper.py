
# Get SOF for crop
def get_sof_of_crop(sof_df, crop, land_type):
    sof = 0.0
    # check if land type is there for particular crop, if not return sof for crop irrespective of land type
    if len(sof_df[(sof_df['Crop']==crop) & (sof_df['LandType']==land_type)]) == 0:
        sof = sof_df[sof_df['Crop']==crop]['Scale of Finance (2024-25)'].to_list()[0]
        if "-" in sof:
            sof = float(sof.split('-')[1])
        else:
            sof = float(sof)
    else: 
        res = sof_df[(sof_df['Crop']==crop) & (sof_df['LandType']==land_type)]['Scale of Finance (2024-25)'].to_list()[0]
        if "-" in res:
            sof = float(res.split('-')[1])
        else:
            sof = float(res)
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


