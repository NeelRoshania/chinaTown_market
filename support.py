def nbs(gapi, placeID, restaurants, rating, priceLevel, address, lat, lng, reviews):

    # nearbysearch assume 100 meter radius
    nbs_base = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
    nbs_key = "keyword=" + "chinatown restaurants".replace(" ", "%20")
    nbs_other = "&key="+gapi
    nbs_nextPage = ""
    
    for a in range(len(placeID)):
#         - For each placeID
#         - Do nbs
#         - Iterate through each page of nbs, insert non-duplicates
        nbs_location = "location={},{}&radius=100&type=restaurant&".format(lat[a], lng[a])
        nbs_gurl = nbs_base+nbs_location+nbs_key+nbs_other
        nbs_response = requests.get(nbs_gurl).json()
        
#         Iterate through each page of nbs
        for b in nbs_response["results"]:
            
#             If the place_of the current result is not in the place_id list, then add to list
            if b["place_id"] not in placeID:
                rating.append(b["rating"]) if "rating" in b else rating.append(np.nan)
                restaurants.append(b["name"]) if "name" in b else restaurants.append(np.nan)
                reviews.append(b["user_ratings_total"]) if "user_ratings_total" in b else reviews.append(np.nan)
                priceLevel.append(b["price_level"]) if "price_level" in b else priceLevel.append(np.nan)
                address.append(b["vicinity"]) if "vicinity" in b else address.append(np.nan)
                placeID.append(b["place_id"]) if "place_id" in b else placeID.append(np.nan)
                lat.append(b["geometry"]["location"]["lat"]) if "geometry" in b else lat.append(np.nan)
                lng.append(b["geometry"]["location"]["lng"]) if "geometry" in b else lng.append(np.nan)
                
            if "next_page_token" in nbs_response:
                sleep(np.random.normal(5, 0.1, 1))
                nbs_nextPage = "&pagetoken="+nbs_response["next_page_token"]
                nbs_gurl = nbs_base+nbs_other+nbs_nextPage
        #         print("{}: {}".format(j, nbs_gurl))
                for c in requests.get(nbs_gurl).json()["results"]:
                    if c["place_id"] not in placeID:
                        rating.append(c["rating"]) if "rating" in c else rating.append(np.nan)
                        restaurants.append(c["name"]) if "name" in c else restaurants.append(np.nan)
                        reviews.append(c["user_ratings_total"]) if "user_ratings_total" in c else reviews.append(np.nan)
                        priceLevel.append(c["price_level"]) if "price_level" in c else priceLevel.append(np.nan)
                        address.append(c["vicinity"]) if "vicinity" in c else address.append(np.nan)
                        placeID.append(c["place_id"]) if "place_id" in c else placeID.append(np.nan)
                        lat.append(c["geometry"]["location"]["lat"]) if "geometry" in c else lat.append(np.nan)
                        lng.append(c["geometry"]["location"]["lng"]) if "geometry" in c else lng.append(np.nan)
                    
        #         print("response: {}".format(nbs_response))
            else:
                print(" - nbs next_page_token not found in {}, response: {}".format(a, nbs_response["status"]))
                break
    return [placeID, restaurants, rating, priceLevel, address, lat, lng, reviews]
    
# print(len(data["Name"]), len(data["Rating"]), len(data["Reviews"]), len(data["PriceLevel"]), len(data["Address"]), len(data["placeId"]))
