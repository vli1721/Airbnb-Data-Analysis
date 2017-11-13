from flask import Flask, render_template, request
import pandas as pd
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64

app = Flask(__name__)
data = pd.read_csv("listings.csv")
availData = pd.read_csv("calendar_available_only.csv")


@app.route("/")
def index():
	# Visual 1
	# Set up lists for x and y values in plotting
	neighborhoodList = data["neighbourhood_cleansed"].value_counts()
	neighborhoodListx = list(neighborhoodList.to_dict().keys())
	neighborhoodListy = neighborhoodList.tolist()

	img = BytesIO()

	# Plot Visual 1 data in bar graph
	plt.bar(neighborhoodListx, neighborhoodListy)
	plt.xticks(np.arange(len(neighborhoodListx)), rotation='vertical')
	plt.xlabel("Neighborhood")
	plt.ylabel("Number of Listings")
	plt.title("Airbnb Listings Per Neighborhood in San Francisco")

	# Convert data into base 64 to pass into HTML
	plt.savefig(img, format='png', bbox_inches="tight", pad_inches=0.2)
	img.seek(0)
	bar_url1 = base64.b64encode(img.getvalue()).decode('UTF-8')
	plt.clf()

	# Visual 2
	# Set up lists for x and y values in plotting
	avgReviewsDict = {}
	counter = 0
	for neighborhood in neighborhoodListx:
		avgReviewsDict[neighborhood] = data.loc[data['neighbourhood_cleansed'] == neighborhood, 'review_scores_rating'].sum() / neighborhoodListy[counter]
		counter += 1
	avgReviewsDictx = list(avgReviewsDict.keys())
	avgReviewsDicty = list(avgReviewsDict.values())

	# Plot Visual 2 data in bar graph
	plt.bar(avgReviewsDictx, avgReviewsDicty)
	plt.xticks(np.arange(len(avgReviewsDictx)), rotation='vertical')
	plt.xlabel("Neighborhood")
	plt.ylabel("Average Review of Listing")
	plt.title("Average Reviews for Airbnb Listings Per Neighborhood in San Francisco")

	# Convert data into base 64 to pass into HTML
	plt.savefig(img, format='png', bbox_inches="tight", pad_inches=0.2)
	img.seek(0)
	bar_url2 = base64.b64encode(img.getvalue()).decode('UTF-8')
	plt.clf()

	# Visual 3
	# Set up lists for x and y values in plotting
	neighborhoodIDList = data["id"].tolist()
	neighborhoodNameList = data["neighbourhood_cleansed"].tolist()
	neighborhoodNameDict = {}
	for i in range(len(neighborhoodIDList)):
		neighborhoodNameDict[neighborhoodIDList[i]] = neighborhoodNameList[i]
	availableListings = availData["listing_id"].value_counts()
	availableListingsID = list(availableListings.to_dict().keys())
	availableListingsNumDays = availableListings.tolist()
	availableListingsByNeighborhood = {}
	for neighborhood in neighborhoodNameList:
		availableListingsByNeighborhood[neighborhood] =  0
	counter = 0
	for listingID in availableListingsID:
		availableListingsByNeighborhood[neighborhoodNameDict[listingID]] += availableListingsNumDays[counter]
		counter += 1
	availableListingsByNeighborhoodx = list(availableListingsByNeighborhood.keys())
	availableListingsByNeighborhoody = list(availableListingsByNeighborhood.values())

	# Plot Visual 3 data in bar graph
	plt.bar(availableListingsByNeighborhoodx, availableListingsByNeighborhoody)
	plt.xticks(np.arange(len(availableListingsByNeighborhoodx)), rotation='vertical')
	plt.xlabel("Neighborhood")
	plt.ylabel("Number of Total Available Days")
	plt.title("Listing Availability By Neighborhood in San Francisco")

	# Convert data into base 64 to pass into HTML
	plt.savefig(img, format='png', bbox_inches="tight", pad_inches=0.2)
	img.seek(0)
	bar_url3 = base64.b64encode(img.getvalue()).decode('UTF-8')
	plt.clf()

	return render_template("index.html", img1=bar_url1, img2=bar_url2, img3=bar_url3)


@app.route("/estimate", methods=["GET", "POST"])
def estimate():

	# If page is accessed via POST request
	if request.method == "POST":

		# Ensure that user inputted valid coordinates
		try:
			latitude = float(request.form.get("latitude"))
		except ValueError:
			return render_template("error.html", message="Enter a valid latitude")
		try:
			longitude = float(request.form.get("longitude"))
		except ValueError:
			return render_template("error.html", message="Enter a valid longitude")

		weeklyIncomeSum = 0
		numProperties = 0

		# Iterate through properties that are within 0.01 degrees latitude and 0.01 degrees longitude of given geolocation
		for index, row in data.iterrows():
			if abs(float(row['latitude']) - latitude) < 0.01 and abs(float(row['longitude']) - longitude) < 0.01:

				# Calculate how many days each property was booked in one year
				annualNumBooked = 365 - int(row['availability_365'])

				# Assume each day earns an average of the total amount earned per year (divide total income by 365 days)
				weeklyIncomeSum += float(row['price'][1:].replace(",", "")) * annualNumBooked / 365 * 7
				numProperties += 1

		# Check if no nearby properties were found
		if numProperties == 0:
			return render_template("error.html", message="No properties were found near the inputted geolocation")

		# Compute average weekly income for property within 0.01 degrees latitude and 0.01 degrees longitude of given geolocation
		weeklyIncomeAvg = str("%.2f" %(weeklyIncomeSum / numProperties))

		return render_template("estimated.html", latitude=latitude, longitude=longitude, weeklyIncomeAvg=weeklyIncomeAvg)

	# If page is accessed via GET request
	else:
		return render_template("estimate.html")


@app.route("/optimize", methods=["GET", "POST"])
def optimize():

	# If page is accessed via POST request
	if request.method == "POST":

		# Ensure that user inputs are valid
		try:
			latitude = float(request.form.get("latitude"))
		except ValueError:
			return render_template("error.html", message="Enter a valid latitude")
		try:
			longitude = float(request.form.get("longitude"))
		except ValueError:
			return render_template("error.html", message="Enter a valid longitude")
		try:
			bedrooms = int(request.form.get("bedrooms"))
		except ValueError:
			return render_template("error.html", message="Enter a valid number of bedrooms")
		try:
			bathrooms = int(request.form.get("bathrooms"))
		except ValueError:
			return render_template("error.html", message="Enter a valid number of bathrooms")
		try:
			optimizeDays = int(request.form.get("optimizeType"))
		except TypeError:
			return render_template("error.html", message="Enter a valid optimization type")

		nearbyPropertiesPrice = {}
		nearbyPropertiesIncome = {}

		# Iterate through properties and determine total income from ones that are within 0.01 degrees latitude and 0.01 degrees of inputted geolocation
		# and that have the same number of bathrooms and same number of bedrooms
		for index, row in data.iterrows():
			# Ensure that number of bedrooms and number of bathrooms in current row are not NULL
			try:
				int(row['bedrooms'])
			except ValueError:
				continue
			try:
				int(row['bathrooms'])
			except ValueError:
				continue
			if abs(float(row['latitude']) - latitude) < 0.01 and abs(float(row['longitude']) - longitude) < 0.01 and int(row['bedrooms']) == bedrooms and int(row['bathrooms']) == bathrooms:
				nearbyPropertiesPrice[row['id']] = float(row['price'][1:].replace(",", ""))
				nearbyPropertiesIncome[row['id']] = (optimizeDays - row['availability_' + str(optimizeDays)]) * float(row['price'][1:].replace(",", "")) / optimizeDays
		
		
		# Check if no nearby properties were found
		if not nearbyPropertiesIncome:
			return render_template("error.html", message="No properties were found near the inputted geolocation")

		# Find IDs of top 10 best earning properties within .01 degrees latitude and 0.01 degrees of inputted geolocation
		# and with same number of bathrooms and same number of bedrooms
		nearbyPropertiesTopTen = list(pd.Series(nearbyPropertiesIncome).nlargest(10).to_dict().keys())

		# Determine optimal price per night by averaging price per night of top ten earning properties
		optimalPrice = 0
		for property in nearbyPropertiesTopTen:
			optimalPrice += nearbyPropertiesPrice[property]
		optimalPrice /= len(nearbyPropertiesTopTen)
		optimalPriceStr = str("%.2f" %optimalPrice)

		return render_template("optimized.html", latitude=latitude, longitude=longitude, optimalPrice=optimalPriceStr)


	# If page is accessed via GET request
	else:
		return render_template("optimize.html")

if __name__ == '__main__':
	app.run(debug=True)