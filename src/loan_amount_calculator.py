
def calcKisaanLoan(predictedYield, crop_cost):
    amount = predictedYield * float(crop_cost) * 2.47105 #SoF is per acre, farmer request area is in hectares
    return amount