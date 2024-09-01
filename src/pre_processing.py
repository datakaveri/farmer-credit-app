def pre_process_datasets(yield_df, sof_df, apmc_df):
        #yield is in hectares
        #requested area for loan is in hectares
        #sof is in Rs/Acre
        #apmc is in Rs/quintal
        #convert yield year to 2024 or 2023
        # yield_df['year'] = yield_df.apply(lambda row: '2023' if row['year']=='2023-01-01' else '2024', axis=1)
        yield_df['district'] = yield_df['district'].apply(str.lower)
        yield_df['crop'] = yield_df['crop'].apply(str.lower)
        yield_df['season'] = yield_df['season'].apply(str.lower)

        sof_df['Crop'] = sof_df['Crop'].apply(str.lower)
        sof_df['(Irr: irrigated / UI: un-irrigated)'] = sof_df['(Irr: irrigated / UI: un-irrigated)'].apply(str.lower)

        apmc_df['district'] = apmc_df['district'].apply(str.lower)
        apmc_df['crop'] = apmc_df['crop'].apply(str.lower)
        apmc_df['season'] = apmc_df['season'].apply(str.lower)

        return yield_df, sof_df, apmc_df