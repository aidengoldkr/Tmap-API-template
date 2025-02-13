import requests

t_map_api_key = '' #api key 발급 받아서 넣어주세요요

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
        'version' : 1,
        'searchKeyword' : keyword_e,
        'searchType' : 'all',
    }
    
    x_y_response = requests.get(x_y_url, headers=headers, params=x_y_params)
    try:
        x_y_data = x_y_response.json()

        x = x_y_data['searchPoiInfo']['pois']['poi'][0]['newAddressList']['newAddress'][0]['centerLon']
        y = x_y_data['searchPoiInfo']['pois']['poi'][0]['newAddressList']['newAddress'][0]['centerLat']
        address = x_y_data['searchPoiInfo']['pois']['poi'][0]['newAddressList']['newAddress'][0]['fullAddressRoad']
        return (x,y,address,keyword_e)
    except:  # noqa: E722
        print("장소를 찾을 수 없습니다")
        exit()

def get_car_route(s_x,s_y,e_x,e_y,s_n,e_n):
    route_c_url = 'https://apis.openapi.sk.com/tmap/routes'
    headers = t_map_header()

    route_c_parms = {
        'version' : 1,
        'startX' : s_x,
        'startY' : s_y,
        'startName' : s_n,
        'endX' : e_x,
        'endY' : e_y,
        'endName' : e_n
    }

    route_c_response = requests.get(route_c_url, headers=headers, params=route_c_parms)
    route_c_data =route_c_response.json()

    distance = route_c_data['features'][0]['properties']['totalDistance']
    time = route_c_data['features'][0]['properties']['totalTime']
    fare = route_c_data['features'][0]['properties']['totalFare']
    texi = route_c_data['features'][0]['properties']['taxiFare']
    return(distance,time,fare,texi)

def get_walk_route(s_x,s_y,e_x,e_y,s_n,e_n):
    route_w_url = 'https://apis.openapi.sk.com/tmap/routes/pedestrian'
    headers = t_map_header()

    route_w_parms = {
        'version' : 1,
        'startX' : s_x,
        'startY' : s_y,
        'startName' : s_n,
        'endX' : e_x,
        'endY' : e_y,
        'endName' : e_n
    }
    
    route_w_response = requests.get(route_w_url, headers=headers, params=route_w_parms)
    route_w_data = route_w_response.json()
    if 'error' in route_w_data:
        return(None,None, "도보 검색을 지원하지 않는 구간입니다")
    else:
        distance = route_w_data['features'][0]['properties']['totalDistance']
        time = route_w_data['features'][0]['properties']['totalTime']
        return(distance,time, "도보")

def get_public_route(s_x,s_y,e_x,e_y): 
    route_p_url = 'https://apis.openapi.sk.com/transit/routes'
    headers = t_map_header()

    route_p_parms = {
        'startX' : s_x,
        'startY' : s_y,
        'endX' : e_x,
        'endY' : e_y, 
    }

    route_p_response = requests.post(route_p_url, json=route_p_parms, headers=headers)
    route_p_data = route_p_response.json()
    buscount = route_p_data['metaData']['requestParameters']['busCount']
    subwaycount = route_p_data['metaData']['requestParameters']['subwayCount']
    bus_subwaycount = route_p_data['metaData']['requestParameters']['subwayBusCount']
    route_data= route_p_data['metaData']['plan']['itineraries']
        
    bus_route = []
    subway_route = []
    busubway_route = []
    for i in route_data:
        isbus, issubway = False,False
        data_list = [i['fare']['regular']['totalFare'],i['totalTime'],i['totalDistance'],i['totalWalkTime'],i['totalWalkDistance']]
        for j in i["legs"]:
                if j['mode'] == 'WALK':
                    public_list_append = [j['mode'],j['sectionTime'],j['distance'],j['start']['name'],j['end']['name'],None]
                elif j['mode'] == 'BUS':
                    public_list_append = [j['mode'],j['sectionTime'],j['distance'],j['start']['name'],j['end']['name'],j['route']]
                    isbus = True
                elif j['mode'] == 'SUBWAY':
                    public_list_append = [j['mode'],j['sectionTime'],j['distance'],j['start']['name'],j['end']['name'],j['route']]
                    issubway = True
                data_list.append(public_list_append)
        if isbus and issubway:
            busubway_route.append(data_list)
        elif isbus:
             bus_route.append(data_list)
        elif issubway:
             subway_route.append(data_list)

    return(buscount,subwaycount,bus_subwaycount, bus_route,subway_route,busubway_route)

