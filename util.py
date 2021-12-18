from geopy import distance
import datetime

def get_current_datetime():
    return datetime.date.today()


def get_future_datetime():
    td = datetime.timedelta(days=365)
    return datetime.date.today() + td


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


