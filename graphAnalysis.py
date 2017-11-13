import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv("listings.csv")
neighborhoodList = data["neighbourhood_cleansed"].value_counts()
neighborhoodListx = list(neighborhoodList.to_dict().keys())
neighborhoodListy = neighborhoodList.tolist()
#print(neighborhoodListx)
#print(neighborhoodListy)
# plt.bar(neighborhoodListx, neighborhoodListy)
# plt.xticks(np.arange(len(neighborhoodListx)), rotation='vertical')
# plt.xlabel("Neighborhood")
# plt.ylabel("Number of Listings")
# plt.title("Airbnb Listings Per Neighborhood in San Francisco")
# plt.show()
# print(plt.rcParams["figure.figsize"])
#neighborhoodList2 = data["neighbourhood_cleansed"].tolist()
#priceList = data["price"].tolist()
# avgReviewsDict = {}
# counter = 0
# for neighborhood in neighborhoodListx:
# 	avgReviewsDict[neighborhood] = data.loc[data['neighbourhood_cleansed'] == neighborhood, 'review_scores_rating'].sum() / neighborhoodListy[counter]
# 	counter += 1
# avgReviewsDictx = list(avgReviewsDict.keys())
# avgReviewsDicty = list(avgReviewsDict.values())

#priceData = data[['neighbourhood_cleansed','price']]
#for neighborhood in priceData:
#print(avgReviewsDict)
#print(avgReviewsDictx)
#print(avgReviewsDicty)

# neighborhoodIDList = data["id"].tolist()
# neighborhoodNameList = data["neighbourhood_cleansed"].tolist()
# neighborhoodNameDict = {}
# for i in range(len(neighborhoodIDList)):
# 	neighborhoodNameDict[neighborhoodIDList[i]] = neighborhoodNameList[i]
# availData = pd.read_csv("calendar_available_only.csv")

# availableListings = availData["listing_id"].value_counts()
# availableListingsID = list(availableListings.to_dict().keys())
# availableListingsNumDays = availableListings.tolist()

# availableListingsByNeighborhood = {}
# for neighborhood in neighborhoodNameList:
# 	availableListingsByNeighborhood[neighborhood] =  0
# counter = 0
# for listingID in availableListingsID:
# 	availableListingsByNeighborhood[neighborhoodNameDict[listingID]] += availableListingsNumDays[counter]
# 	counter += 1

# availableListingsByNeighborhoodx = list(availableListingsByNeighborhood.keys())
# availableListingsByNeighborhoody = list(availableListingsByNeighborhood.values())
# print(availableListingsByNeighborhoodx)
# print(availableListingsByNeighborhoody)

# calendar = pd.read_csv("calendar.csv")
# rowCalendar = calendar[calendar['listing_id'] == 8053481]
# numBooked = rowCalendar['available'].value_counts()["t"]

# optimizeDays = 365
# nearbyProperties = {}
# # Iterate through properties
# for index, row in data.iterrows():
# 	if abs(float(row['latitude']) - 37.75418395) < 0.01 and abs(float(row['longitude']) - -122.4065138) < 0.01:
# 		nearbyProperties[row['id']] = optimizeDays - row['availability_' + str(optimizeDays)]
# nearbyPropertiesTopTen = list(pd.Series(nearbyProperties).nlargest(10).to_dict().keys())

# print(nearbyPropertiesTopTen)
bedrooms = 1
bathrooms = 1
optimizeDays = 365
nearbyPropertiesPrice = {}
nearbyPropertiesIncome = {}
# Iterate through properties and determine total income from ones that are within 0.01 degrees latitude and 0.01 degrees of inputted geolocation
for index, row in data.iterrows():
	try:
		int(row['bedrooms'])
	except ValueError:
		continue
	try:
		int(row['bathrooms'])
	except ValueError:
		continue
	if abs(float(row['latitude']) - 37.75418395) < 0.01 and abs(float(row['longitude']) - -122.4065138) < 0.01 and int(row['bedrooms']) == bedrooms and int(row['bathrooms']) == bathrooms:
		nearbyPropertiesPrice[row['id']] = float(row['price'][1:].replace(",", ""))
		nearbyPropertiesIncome[row['id']] = int(optimizeDays - row['availability_' + str(optimizeDays)]) * float(row['price'][1:].replace(",", ""))
# Find IDs of top 10 most booked properties within 0.01 degrees latitude and 0.01 degrees of inputted geolocation
nearbyPropertiesTopTen = list(pd.Series(nearbyPropertiesIncome).nlargest(10).to_dict().keys())
# Determine optimal price per night by averaging 
optimalPrice = 0
nearbyProperties2 = []
for property in nearbyPropertiesTopTen:
	optimalPrice += nearbyPropertiesPrice[property]
	nearbyProperties2.append(nearbyPropertiesPrice[property])
optimalPrice /= 10
optimalPriceStr = str("%.2f" %optimalPrice)
print(optimalPriceStr)
print(nearbyProperties2)

# rowCalendar = calendar[calendar['listing_id'] == row['id']]
# try:
# 	annualNumBooked = rowCalendar['available'].value_counts()["f"]
# except KeyError:
# 	# If no days were available, there will be a KeyError, so set number of booked days to 365
# 	annualNumBooked = 365


#print(neighborhoodList2)
#print(priceList)