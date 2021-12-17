from google_api_folder.places import places
from geopy import distance
import googlemaps

def convert_address(element:dict):
    result={}
    result['formatted_address']=element.get('formatted_address',"") 
    result['place_id']=element.get('place_id',"")
    result['name']=element.get('name',"")
    result['opening_hours']=element.get('opening_hours',"")
    result['rating']=element.get('rating',"")
    result['geometry']=str(element['geometry']['location']['lat'])+","+str(element['geometry']['location']['lng'])
    return result

def calculate_distance(element1,element2):
    element1_coordonates = element1['geometry'].split(",")
    element2_coordonates = element2['geometry'].split(",")
    return distance.distance(element1_coordonates,element2_coordonates).km

def get_clean_closest_locations(locations,base_location=None):
    result = [convert_address(element) for element in locations['results']]
    for element in result:
        element['temp_distance']=calculate_distance(element,base_location)
    result2=sorted(result, key = lambda i:i['temp_distance'])
    return result2
    
gmaps = googlemaps.Client(key='AIzaSyDd9PEXWCwFICDLbufYsDl2D5R6XOshzo4')

#Default Test Values
search_string="Urgente ginecolog"
current_home_address="Strada Semilunei 4-6, București 020797"

geocode_home_address =convert_address(gmaps.geocode(current_home_address)[0])

locations = places(gmaps,query=search_string,location=geocode_home_address['geometry'],radius=5000,language="ro",type="doctor")

sorted_locations = get_clean_closest_locations(locations,geocode_home_address)

print(str(sorted_locations))

