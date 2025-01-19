from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
import utility as u

debuging_mode = False
able_bike = False
# start_input = input("출발지를 입력하세요") 
# end_input = input("도착지를 입력하세요")

start_input = '덕소중학교'
end_input = '헬로알고'

start_x, start_y = u.get_x_y_ep(start_input)
end_x, end_y = u.get_x_y_ep(end_input)
start_x_, start_y_ = u.get_x_y(start_input)
end_x_, end_y_ = u.get_x_y(end_input)

options = webdriver.ChromeOptions()
# options.add_argument("headless")  # 브라우저가 보이지 않도록 설정
# options.add_experimental_option("detach", True)
options.add_argument("disable-gpu")  # GPU 비활성화 (Linux 환경에서 이 설정을 자주 사용)
options.add_argument("disable-dev-shm-usage")  # 공유 메모리 사용 비활성화
options.add_argument("disable-extensions")  # 불필요한 확장 프로그램 비활성화
# options.add_argument("--blink-settings=imagesEnabled=false")
options.add_argument("disable-logging")  # 로그 비활성화
options.add_argument("log-level=3")
    
service = Service(ChromeDriverManager().install()) 
driver = webdriver.Chrome(service=service, options=options)
action = ActionChains(driver)

def get_optimal_route(r_e):
    remove_keywords = ['최적', '최소도보', '최소환승', '최소시간','다음날']
    final_route = None
    walk_10_flag = False
    over_1am = False
    for_start = 4
    route_mini = []
    w10sq = []
    r = []

    current_hour = time.localtime().tm_hour
    if 1 <= current_hour < 5:
        over_1am = True

    for i in r_e:
        r.append(i.get_attribute("innerText").split('\n'))

    for i in r:
            if i[0] in remove_keywords:
                i.pop(0)
            if i[1] in remove_keywords:
                i.pop(1)
            
    for i in r:
        list_a = []
        for j in range(3,len(i),2):
            if '분' == i[j+1][-1]:
                list_a.append([i[j], int(i[j+1][:-1])])
            else:
                break
        route_mini.append(list_a)
    
    route_mini_sorted = sorted(route_mini, key=len)
    if debuging_mode:
        print(r)
        print(route_mini)
        print(route_mini_sorted)
    for i in route_mini_sorted:
        for j in i:
            if j[0] == '도보':
                if j[1] >= 10:
                    final_route = i
                    walk_10_flag = True
                    w10sq.append(i.index(j))

        if walk_10_flag:
            break    

    if walk_10_flag:
        route_seq = route_mini.index(final_route)
    else:
        route_seq = 0
    
    return (route_seq,w10sq)

def make_detail_route(w10sq,d_r_r,d_t_r):
    d_t = []
    d_r = []
    replace_walk_pair = []

    for i in d_r_r:
        d_r.append(i.get_attribute("innerText"))
    for i in d_t_r:
        d_t.append('>>> ' + f'{i.get_attribute("innerText").replace('\n',' ')}')

    for i in range(len(d_r)):
        if '승차' in d_r[i]:
            d_r[i] = d_r[i].split('승차')[0].strip()
        elif '하차' in d_r[i]:
            d_r[i] = d_r[i].split('하차')[0].strip()
    
    len_d_r = len(d_r) -1
    route_seq_list = [0] * len_d_r

    for i in w10sq:
        replace_walk_pair.append([d_r[i-1],d_r[i]])
        route_seq_list[i-1] = 1



    return(d_r,d_t,replace_walk_pair,route_seq_list)

def make_ddareuungi_route(replace_walk_pair,w10sq):
    start_bike_s = []
    end_bike_s = []
    start_bike_info = []
    end_bike_info = []
    counter_1 = 0

    for i in replace_walk_pair:
        ws_x,ws_y = u.get_x_y(i[0])
        we_x,we_y = u.get_x_y(i[1])
        print(ws_x,ws_y)
        bs_s = u.find_Ddareuungi_station(float(ws_y),float(ws_x))
        bs_e = u.find_Ddareuungi_station(float(we_y),float(we_x))
        print('done12')
        if bs_s != 0 and bs_e != 0:
            start_bike_s.append(bs_s)
            end_bike_s.append(bs_e)
        else:
            del w10sq[counter_1]
            continue
        counter_1 += 1

    for i in start_bike_s:
            adress = u.reverse_geo(i[1],i[2])
            start_bike_info.append([i[0],adress,i[4],i[5]])

    for i in end_bike_s:
            adress = u.reverse_geo(i[1],i[2])
            end_bike_info.append([i[0],adress,i[4],i[5]])

    return(start_bike_info,end_bike_info)

def make_final_route(route_seq_list, detail_route, detail_transport, replace_walk_pair, start_bike_info, end_bike_info):
    final_route = []
    route_count = 0
    bike_count = 0

    for i in range(len(route_seq_list)):
        final_route.append(detail_route[route_count])

        if route_seq_list[i] == 1:
            start, end = replace_walk_pair[bike_count]
            final_route.append(f">>> 도보 {start_bike_info[bike_count][3]}m")
            final_route.append(f"{start_bike_info[bike_count][0]} ({start_bike_info[bike_count][1]}) 잔여대수 : {start_bike_info[bike_count][2]}")
            final_route.append(">>> 따릉이 이동")
            final_route.append(f"{end_bike_info[bike_count][0]} ({end_bike_info[bike_count][1]})")
            final_route.append(f">>> 도보 {end_bike_info[bike_count][3]}m")
            bike_count += 1
        else:
            final_route.append(detail_transport[i])

        route_count += 1

    final_route.append(detail_route[route_count])
    return final_route

driver.get(f"https://map.naver.com/p/directions/{start_x},{start_y},{start_input}/{end_x},{end_y},{end_input}/-/transit?")
WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class = "item_btn"]')))
route_elements = driver.find_elements(By.XPATH, '//div[@class = "item_btn"]')

route_seq, walk_10_seq = get_optimal_route(route_elements)
      
action.move_to_element(route_elements[route_seq]).perform()
route_elements[route_seq].click()
route_elements[route_seq].click()


# WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="panel_content_wrap"]')))
detail_route_r = driver.find_elements(By.XPATH, '//strong[@class = "path_title"]')
detail_transport_r = driver.find_elements(By.XPATH, '//div[@class = "detail_step_icon_area"]')

detail_route, detail_transport, replace_walk_pair, route_seq_list = make_detail_route(walk_10_seq,detail_route_r,detail_transport_r)

if debuging_mode:
    print(detail_route, detail_transport, replace_walk_pair, route_seq_list, sep= '\n')

if able_bike:
    start_bike_info, end_bike_info = make_ddareuungi_route(replace_walk_pair,walk_10_seq)
else:
    start_bike_info =[]
    end_bike_info = []
    replace_walk_pair = []
    len_d_r = len(detail_route) -1
    route_seq_list = [0] * len_d_r

final_route = make_final_route(route_seq_list, detail_route, detail_transport, replace_walk_pair, start_bike_info, end_bike_info)

for i in final_route:
    print(i, end='\n')