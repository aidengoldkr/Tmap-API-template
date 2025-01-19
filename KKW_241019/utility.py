import requests
from haversine import haversine

t_map_api_key = 'n8zsIWsyk34hbmYfX4PzbjN4CKizkXD3FdvGi5ig'

def t_map_header():
    headers = {
    'appKey': t_map_api_key,
    'Content-Type': 'application/json'
    }
    return(headers)

def get_x_y(keyword):
    x_y_url = 'https://apis.openapi.sk.com/tmap/pois'
    headers = t_map_header()
    keyword_e = keyword.encode('utf-8')

    x_y_params = {
        'version': 1,
        'searchKeyword': keyword_e,
        'searchType': 'all',
    }

    x_y_response = requests.get(x_y_url, headers=headers, params=x_y_params)
    try:
        x_y_data = x_y_response.json()

        x = x_y_data['searchPoiInfo']['pois']['poi'][0]['newAddressList']['newAddress'][0]['centerLon']
        y = x_y_data['searchPoiInfo']['pois']['poi'][0]['newAddressList']['newAddress'][0]['centerLat']
        return(x, y)
    except:
        print("잘못된 출발지, 목적지 정보 입니다")
        exit()

def get_x_y_ep(keyword):
    x_y_url = 'https://apis.openapi.sk.com/tmap/pois'
    headers = t_map_header()
    keyword_e = keyword.encode('utf-8')

    x_y_params = {
        'version': 1,
        'searchKeyword': keyword_e,
        'searchType': 'all',
        'resCoordType': 'EPSG3857'
    }

    x_y_response = requests.get(x_y_url, headers=headers, params=x_y_params)
    try:
        x_y_data = x_y_response.json()

        x = x_y_data['searchPoiInfo']['pois']['poi'][0]['newAddressList']['newAddress'][0]['centerLon']
        y = x_y_data['searchPoiInfo']['pois']['poi'][0]['newAddressList']['newAddress'][0]['centerLat']
        return(x, y)
    except:
        print("잘못된 출발지, 목적지 정보 입니다")
        exit()

def find_Ddareuungi_station(lat, lon, radius=1):
    Ddareuungi_url_1 = 'http://openapi.seoul.go.kr:8088/545666646e6169643833456d794e4d/json/bikeList/1/1000/'
    Ddareuungi_url_2 = 'http://openapi.seoul.go.kr:8088/545666646e6169643833456d794e4d/json/bikeList/1001/2000/'

    Ddareuungi_response_1 = requests.get(Ddareuungi_url_1)
    Ddareuungi_response_2 = requests.get(Ddareuungi_url_2)

    Ddareuungi_data_1 = Ddareuungi_response_1.json()
    Ddareuungi_data_2 = Ddareuungi_response_2.json()

    station_list = Ddareuungi_data_1['rentBikeStatus']['row'] + Ddareuungi_data_2['rentBikeStatus']['row']

    station_result = []
    for i in station_list:
        s_lat = float(i['stationLatitude'])
        s_lon = float(i['stationLongitude'])
        dis_gap = haversine((lat, lon), (s_lat, s_lon))
        if dis_gap <= radius:
            if int(i['parkingBikeTotCnt']) > 0:
                if i not in station_result:
                    station_result.append([i['stationName'],i['stationLatitude'],i['stationLongitude'],i['stationId'],int(i['parkingBikeTotCnt']),float(f"{dis_gap*1000:.1f}")])
    
    radius_stations = sorted(station_result, key=lambda x: x[5])
    try:
        return radius_stations[0]
    except:
        return 0
def reverse_geo(lat,lon):
    r_geo_url = 'https://apis.openapi.sk.com/tmap/geo/reversegeocoding'
    headers = t_map_header()

    r_geo_parms = {
        'version': 1,       
        'lon' : lon,
        'lat' : lat,
        'addressType' : 'A02'
    }

    r_geo_response = requests.get(r_geo_url, headers=headers, params=r_geo_parms)
    r_geo_data = r_geo_response.json()

    return(r_geo_data['addressInfo']['fullAddress'])