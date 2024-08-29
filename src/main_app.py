import pandas as pd
import validator as val

class MainApp:
    def __init__(self):
        # yield_df = pd.DataFrame()
        # sof_df = pd.DataFrame()
        # apmc_df = pd.DataFrame()
        self.yield_df = self.load_datasets('dataset/yield_pred_2023_2024.csv', 'csv')
        self.sof_df = self.load_datasets('dataset/SOF-TS.xlsx', 'xlsx')
        self.apmc_df = self.load_datasets('dataset/apmc_historical_data.csv', 'csv')
        self.crop_name = ''
        self.crop_area = ''
        self.district = ''
        self.season = ''

    def load_datasets(self, filename, file_format):
        if file_format == 'csv':
            df =  pd.read_csv(filename)
        if file_format == 'xlsx':
            df = pd.read_excel(filename, sheet_name='2023-2025')
        return df
    
    def pre_process_datasets(self, df):
        return df


    def main_process(self, config):
        #get PPB 
        status = "success"
        response = {"kissan_loan_amount":0.0,
                    "consumer_loan_amount": 0.0}
        

        ##################### Start: Read Config Params #####################
        
        self.crop_name = config['crop_name']
        self.crop_area = float(config['area_in_hectares'])
        self.season = config['season']
        self.district = config['district']

        ##################### End: Read Config Params #####################

        ##################### Start: Validations #####################
        
        if self.crop_name not in self.yield_df['crop'].unique():
            print("Invalid crop name")
            status='failed'

        # check if crop area is valid
        if not val.validate_area(self.crop_area):
            print("Invalid crop area")
            print("Not elegible for kissan loan")
            status='failed'
            response = {}
        
        #check if season is valid
        if self.season not in self.yield_df['season'].unique():
            print("Invalid season")
            status='failed'
            response = {}

        # validate if crop is grown in the selected season & selected district
        if not val.validate_crop(self.crop_name, self.season, self.district, self.yield_df):
            print("Crop is not grown in the selected season & district")
            print("Not elegible for kissan loan")
            status='failed'
            response = {}

        # do a check on if yield of crop is decreasing over the years
        # if yield is decreasing, then do not give loan
        if not val.yield_decreasing(self.crop_name):
            print("Yield of the crop is decreasing over the years")
            print("Not elegible for kissan loan")
            status='failed'
            response = {}
        print('Completed validations successfully')
        ##################### End: Validations #####################


        ##################### Start: Preprocess Datasets #####################
        #yield is in hectares
        #requested area for loan is in hectares
        #sof is in Rs/Acre
        #apmc is in Rs/quintal
        #convert yield year to 2024 or 2023
        self.yield_df['year'] = self.yield_df.apply(lambda row: '2023' if row['year']=='2023-01-01' else '2024', axis=1)
        self.yield_df['district'] = self.yield_df['district'].apply(str.lower)
        self.yield_df['crop'] = self.yield_df['crop'].apply(str.lower)
        self.yield_df['season'] = self.yield_df['season'].apply(str.lower)

        self.sof_df['Crop'] = self.sof_df['Crop'].apply(str.lower)

        # self.apmc_df['year'] = self.apmc_df.apply(lambda row: '2023' if row['year']=='2023-01-01' else '2024', axis=1)
        self.apmc_df['district'] = self.apmc_df['district'].apply(str.lower)
        self.apmc_df['crop'] = self.apmc_df['crop'].apply(str.lower)
        self.apmc_df['season'] = self.apmc_df['season'].apply(str.lower)

        ##################### End: Preprocess Datasets #####################


        ##################### Start: Calculate Loan #####################
        kissan_loan = 0.0 #TODO: get the amount from a function
        consumer_loan = 0.0 #TODO: get the amount from a function

        response = {"kissan_loan_amount": kissan_loan,
                    "consumer_loan_amount": consumer_loan}

        ##################### End: Calculate Loan #####################

                
        return status, response