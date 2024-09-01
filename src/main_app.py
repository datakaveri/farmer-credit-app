import pandas as pd
from validator import AppValidator
from loan_amount_calculator import loanCalculator
from pre_processing import pre_process_datasets

class MainApp:
    def __init__(self, config):
        # yield_df = pd.DataFrame()
        # sof_df = pd.DataFrame()
        # apmc_df = pd.DataFrame()
        self.yield_df = self.load_datasets('dataset/yield_pred_2023_2024.csv', 'csv')
        self.sof_df = self.load_datasets('dataset/SOF-TS.xlsx', 'xlsx')
        self.apmc_df = self.load_datasets('dataset/apmc_historical_data.csv', 'csv')
        self.crop_name = config['crop_name']
        self.crop_area = float(config['area_in_hectares'])
        self.district = config['district']
        self.season = config['season']
        self.year = config['year']
        

    def load_datasets(self, filename, file_format):
        if file_format == 'csv':
            df =  pd.read_csv(filename, dtype='str')
        if file_format == 'xlsx':
            df = pd.read_excel(filename, sheet_name='2023-2025', dtype='str')
        df.fillna('', inplace=True)
        return df
    
    def main_process(self):
        #get PPB 
        status = "success"
        kissan_loan = 0.0 
        consumer_loan = 0.0 
        response = {"kissan_loan_amount":kissan_loan,
                    "consumer_loan_amount": consumer_loan}
        
        ##################### Start: Preprocess Datasets #####################
        self.yield_df, self.sof_df, self.apmc_df = pre_process_datasets(self.yield_df, self.sof_df, self.apmc_df)
        ##################### End: Preprocess Datasets #####################

        ##################### Start: Validations #####################
        validator_obj = AppValidator(self.crop_name, self.crop_area, self.season, self.district)
        if not validator_obj.validate(self.yield_df):
            status='failed'
            response = {}
            return status, response        
        print('Completed validations successfully')
        ##################### End: Validations #####################

        ##################### Start: Calculate Loan #####################        
        loan_calculator_obj = loanCalculator(self.crop_name, self.crop_area, self.season, self.district, self.year)
        kissan_loan, consumer_loan = loan_calculator_obj.get_loan_amount(self.yield_df, self.sof_df, self.apmc_df)        
        response = {"kissan_loan_amount": kissan_loan,
                    "consumer_loan_amount": consumer_loan}
        ##################### End: Calculate Loan #####################
                
        return status, response