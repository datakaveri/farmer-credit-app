
# Get SOF for crop
def get_sof_of_crop(sof_df, crop, land_type):
    sof = 0.0
    res = sof_df[(sof_df['Crop']==crop) & (sof_df['LandType']==land_type)]['Scale of Finance (2024-25)'].to_list()[0]
    if "-" in res:
        sof = float(res.split('-')[1])
    else:
        sof = float(res)
    return sof

# get APMC price for the crop
#def get_apmc_price(apmc_df, crop, district):

