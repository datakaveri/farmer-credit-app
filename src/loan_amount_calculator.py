class loanCalculator:
    def __init__(self, crop_name, crop_area, season, district, year):
        self.crop_name = crop_name
        self.crop_area = float(crop_area)
        self.season = season
        self.district = district
        self.year = year
        self.conversion_factor_hec_to_acre = 2.47105 #Convert Hectares to acre
        self.conversion_factor_ton_to_quint = 10    

    def get_kissan_loan(self, crop_sof):
        amount = float(self.crop_area) * float(crop_sof) * self.conversion_factor_hec_to_acre #SoF is per acre, farmer request area is in hectares
        return amount
    
    def get_sof_of_crop(self, sof_df, type_of_land=""):
        sof = 0.0
        res = sof_df[(sof_df['Crop']==self.crop_name) & (sof_df['(Irr: irrigated / UI: un-irrigated)']==type_of_land)]['Scale of Finance (2023-24)'].to_list()[0]
        if "-" in res:
            sof = float(res.split('-')[1])
        else:
            sof = float(res)
        return sof
    
    def get_pred_yield(self, yield_df):
        res = 0.0
        res = yield_df[(yield_df['crop']==self.crop_name) & (yield_df['district']==self.district) & (yield_df['season']==self.season) & (yield_df['year']==self.year)]['yield'].to_list()[0]
        res = float(res)
        return res
    
    def get_pred_apmc(self, apmc_df):
        res = 0.0
        res = apmc_df[(apmc_df['crop']==self.crop_name) & (apmc_df['district']==self.district) & (apmc_df['season']==self.season) & (apmc_df['year']==self.year)]['price'].to_list()[0]
        res = float(res)
        return res
    
    def get_consumer_loan_amount(self, pred_yield, pred_prices, cost_price):
        selling_price = float(pred_yield) * float(self.crop_area) * float(pred_prices) * self.conversion_factor_ton_to_quint #pred_prices are Rs. per quintal
        profit = max(0, selling_price - cost_price)

        return profit

    def get_loan_amount(self, yield_df, sof_df, apmc_df):
        sof_amount = self.get_sof_of_crop(sof_df, 'irr')
        kissan_loan = self.get_kissan_loan(sof_amount)
        yield_pred = self.get_pred_yield(yield_df)
        apmc_pred = self.get_pred_apmc(apmc_df)
        consumer_loan = self.get_consumer_loan_amount(yield_pred, apmc_pred, kissan_loan)
        return kissan_loan, consumer_loan