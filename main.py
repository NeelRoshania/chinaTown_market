# import libraries
import requests
import pandas as pd
import numpy as np
from time import sleep
from support import nbs

# Initializing
restaurants = []
rating = []
reviews = []
priceLevel = []
address = []
placeID = []
lat = []
lng = []

# request setup
gapi = "AIzaSyDl-b0qd8yXxpTmUrW1rSFtZQHvbaYBGNw"
ts_base = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
ts_query = "query=" + "restaurants in chinatown&".replace(" ", "%20")
ts_location = "location=42.3500641,-71.0624052&radius=50000&type=restaurant&"
ts_other = "&key="+gapi
ts_nextPage = ""
ts_gurl = ts_base+ts_query+ts_location+ts_other
ts_response = requests.get(ts_gurl).json()

print("Starting textsearch...")
for j in range(0,5):
    print("- ts page {}".format(j))
    print("\t- Total places: {}".format(len(placeID)))
#     Extract through initial list
    for i in ts_response["results"]:
        if i["place_id"] not in placeID:
            rating.append(i["rating"]) if "rating" in i else rating.append(np.nan)
            restaurants.append(i["name"]) if "name" in i else restaurants.append(np.nan)
            reviews.append(i["user_ratings_total"]) if "user_ratings_total" in i else reviews.append(np.nan)
            priceLevel.append(i["price_level"]) if "price_level" in i else priceLevel.append(np.nan)
            address.append(i["vicinity"]) if "vicinity" in i else address.append(np.nan)
            placeID.append(i["place_id"]) if "place_id" in i else placeID.append(np.nan)
            lat.append(i["geometry"]["location"]["lat"]) if "geometry" in i else lat.append(np.nan)
            lng.append(i["geometry"]["location"]["lng"]) if "geometry" in i else lng.append(np.nan)
            
#     Perform nearby search
    placeID, restaurants, rating, priceLevel, address, lat, lng, reviews = nbs(gapi, placeID, restaurants, rating, priceLevel, address, lat, lng, reviews)
    
#     Iterate to next page
    if "next_page_token" in ts_response:
        sleep(np.random.normal(5, 0.1, 1))
        ts_nextPage = "&pagetoken="+ts_response["next_page_token"]
        ts_gurl = ts_base+ts_other+ts_nextPage
#         print("{}: {}".format(j, ts_gurl))
        ts_response = requests.get(ts_gurl).json()
#         print("response: {}".format(ts_response))
    else:
        print(" - ts next_page_token not found in {}, response: {}".format(j, ts_response["status"]))
        break

print("text search scraping done...!")
data_ts = {"Name": restaurants, "Rating":rating, "Reviews":reviews, 
           "PriceLevel":priceLevel, "Address":address, "placeId":placeID,
           "lat":lat, "lng":lng}

dfts = pd.DataFrame(data=data_ts)
print(len(data_ts["Name"]), len(data_ts["Rating"]), len(data_ts["Reviews"]), len(data_ts["PriceLevel"]), len(data_ts["Address"]), len(data_ts["placeId"]))
