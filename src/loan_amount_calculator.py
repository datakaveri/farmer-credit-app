
def calcKisaanLoan(crop_area, crop_sof):
    amount = crop_area * float(crop_sof) * 2.47105 #SoF is per acre, farmer request area is in hectares
    return amount

def calcConsumerLoan(predictedYield, crop_cost, crop_price):
    selling_price = predictedYield * crop_price * 10  #pred_prices are Rs. per quintal

    if crop_cost > selling_price:
        print("Crop cost is greater than the selling price")
        return 0
    else:
        print("Profit made by the farmer: ", selling_price - crop_cost)
        return selling_price - crop_cost