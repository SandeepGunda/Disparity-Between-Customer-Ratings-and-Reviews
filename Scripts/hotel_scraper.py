import requests
from bs4 import BeautifulSoup as bs
import csv
import pandas as pd

file = "Hotel-2.0.xlsx"
hotel_names = pd.ExcelFile(file)
df1 = hotel_names.parse('Sheet1')

hotel = []
hotel_amenities = []
hotel_room_types = []
hotel_nearby_hotels = []
hotel_nearby_restaurants = []
hotel_nearby_attractions = []

for page in df1['hotel_website']:
    print(page)
    page_data = requests.get(page)
    soup = bs(page_data.text, "html.parser")

    hotel_id = page.split('-d')[1].split('-')[0]


 
    hotel_info_container = soup.find('div', attrs={'id': 'taplc_location_detail_header_hotels_0'})
    hotel_name = hotel_info_container.find('h1', attrs={'id': 'HEADING'}).text
    hotel_user_rating = hotel_info_container.find('span', attrs={'style': 'font-size:16px;'})['alt'].split(' ')[0]
    hotel_add_str = hotel_info_container.find('span', attrs={'class': 'street-address'}).text.split(",")[0]
    hotel_add_city = hotel_info_container.find('span', attrs={'class': 'locality'}).text.split(",")[0]
    hotel_add_state = hotel_info_container.find('span', attrs={'class': 'locality'}).text.split(", ")[-1].split(" ")[0]
    hotel_add_zip = hotel_info_container.find('span', attrs={'class': 'locality'}).text.split(", ")[-1].split(" ")[1][0:5]

    amenities_table = soup.find('div', attrs={'class': 'ui_columns section_content'})
    amenities = []
    for row in amenities_table.findAll("li"):
        if (not [hotel_id, row.get_text().strip()] in amenities) and (len(row['class']) == 1):
            amenities.append([hotel_id, row.get_text().strip()])

    hotel_details_container = soup.find('div', attrs={'class': 'details-top ui_column is-4'})
    hotel_price_lower = \
    hotel_details_container.find('ul', attrs={'class': 'list price_range'}).find_all('li', attrs={'class': 'item'})[
        1].get_text().split(" (")[0].replace(' ', '').split('-')[0].replace('$', '')
    hotel_price_upper = \
    hotel_details_container.find('ul', attrs={'class': 'list price_range'}).find_all('li', attrs={'class': 'item'})[
        1].get_text().split(" (")[0].replace(' ', '').split('-')[1].replace('$', '')

    hotel_expedia_rating = hotel_details_container.find('div', attrs={'title': 'Hotel class'})
    if (hotel_expedia_rating != None):
        hotel_expedia_rating = float(hotel_expedia_rating['class'][1].split('_')[1].strip()) / 10
    else:
        hotel_expedia_rating = ''

    room_types_table = hotel_details_container.find('ul', attrs={'class': 'list room_types'})
    room_types = []
    for row in room_types_table.findAll("li"):
        if (not row.get_text() in room_types) and (len(row['class']) == 1):
            room_types.append([hotel_id, row.get_text().replace(',','').strip()])

    hotel_total_rooms = \
    hotel_details_container.find('ul', attrs={'class': 'list number_of_rooms'}).find_all('li', attrs={'class': 'item'})[
        1].get_text().replace(',','').strip()


    def nearby_adder(row, nearby_list):
        name = row.div.find('div', attrs={'class': 'poiName'})
        if (name != None):
            name = name.get_text().strip()
        else:
            name = ''

        rating = row.div.find('div', attrs={'class': 'prw_rup prw_common_bubble_rating rating'})
        if (rating != None):
            rating = rating.span['alt'].split(' ')[0].strip()
        else:
            rating = ''

        total_reviews = row.div.find('div', attrs={'class': 'reviewCount'})
        if (total_reviews != None):
            total_reviews = total_reviews.get_text().split(' ')[0].replace(',', '').strip()
        else:
            total_reviews = ''

        distance = row.div.find('div', attrs={'class': 'distance'})
        if (distance != None):
            distance = distance.get_text().split(' ')[0].strip()
        else:
            distance = ''

        return nearby_list.append([hotel_id, name, rating, total_reviews, distance])


    nearby_hotels = soup.find_all('div', attrs={'class': 'prw_rup prw_common_btf_nearby_poi_grid poiGrid hotel'})
    if (nearby_hotels != []):
        nearby_hotels = nearby_hotels[0].find_all('div')[1]
        nearby_hotels_list = []
        for row in nearby_hotels:
            nearby_adder(row, nearby_hotels_list)
        hotel_nearby_hotels.append(nearby_hotels_list)

    nearby_restaurants = soup.find_all('div', attrs={'class': 'prw_rup prw_common_btf_nearby_poi_grid poiGrid eatery'})
    if (nearby_restaurants != []):
        nearby_restaurants = nearby_restaurants[0].find_all('div')[1]
        nearby_restaurants_list = []
        for row in nearby_restaurants:
            nearby_adder(row, nearby_restaurants_list)
        hotel_nearby_restaurants.append(nearby_restaurants_list)

    nearby_attractions = soup.find_all('div',
                                       attrs={'class': 'prw_rup prw_common_btf_nearby_poi_grid poiGrid attraction'})
    if (nearby_attractions != []):
        nearby_attractions = nearby_attractions[0].find_all('div')[1]
        nearby_attractions_list = []
        for row in nearby_attractions:
            nearby_adder(row, nearby_attractions_list)
        hotel_nearby_attractions.append(nearby_attractions_list)

    hotel.append(
        [hotel_id, hotel_name, hotel_user_rating, hotel_expedia_rating, hotel_add_str, hotel_add_city, hotel_add_state,
         hotel_add_zip, hotel_total_rooms, hotel_price_lower, hotel_price_upper])
    hotel_amenities.append(amenities)
    hotel_room_types.append(room_types)


def file_writer(data):
    if (data == hotel):
        for i in range(len(data)):
            writer.writerow(data[i])
    else:
        for i in range(len(data)):
            for j in range(len(data[i])):
                writer.writerow(data[i][j])

with open('hotel.csv', 'a') as csv_file:
    writer = csv.writer(csv_file,lineterminator='\n')
    writer.writerow(['hotel_id','hotel_name', 'hotel_user_rating', 'hotel_expedia_rating', 'hotel_add_str', 'hotel_add_city', 'hotel_add_state', 'hotel_add_zip', 'hotel_total_rooms', 'hotel_price_lower($)', 'hotel_price_upper($)'])
    file_writer(hotel)

with open('amenities.csv', 'a') as csv_file:
    writer = csv.writer(csv_file,lineterminator='\n')
    writer.writerow(['hotel_id','amenity'])
    file_writer(hotel_amenities)

with open('room_types.csv', 'a') as csv_file:
    writer = csv.writer(csv_file,lineterminator='\n')
    writer.writerow(['hotel_id', 'room_type'])
    file_writer(hotel_room_types)

with open('nearby_hotels.csv', 'a') as csv_file:
    writer = csv.writer(csv_file,lineterminator='\n')
    writer.writerow(['hotel_id','nearby_hotel_name','rating','reviews','distance'])
    file_writer(hotel_nearby_hotels)

with open('nearby_restaurants.csv', 'a') as csv_file:
    writer = csv.writer(csv_file,lineterminator='\n')
    writer.writerow(['hotel_id', 'nearby_restaurants_name', 'rating', 'reviews', 'distance'])
    file_writer(hotel_nearby_restaurants)

with open('nearby_attractions.csv', 'a') as csv_file:
    writer = csv.writer(csv_file,lineterminator='\n')
    writer.writerow(['hotel_id', 'nearby_attraction_name', 'rating', 'reviews', 'distance'])
    file_writer(hotel_nearby_attractions)