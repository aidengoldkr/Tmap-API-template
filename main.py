import utility as util

start_keyword = input("출발지를 입력하세요: ")
end_keyword = input("목적지를 입력하세요: ")

start_x, start_y, start_address, start_keyword_e = util.get_x_y(start_keyword)
end_x, end_y, end_address, end_keyword_e = util.get_x_y(end_keyword)


c_distance,c_time,c_fare,texi = util.get_car_route(start_x,start_y,end_x,end_y,start_keyword_e,end_keyword_e)
w_distance,w_time, w_error = util.get_walk_route(start_x,start_y,end_x,end_y,start_keyword_e,end_keyword_e)
bus_count,sub_count,busub_count,bus_data,sub_data,busub_data = util.get_public_route(start_x,start_y,end_x,end_y)
for_list = [bus_data,sub_data, busub_data]
for_list_ = ['버스','지하철','버스 + 지하철']

print(f"\n출발지 : {start_address}")
print(f"목적지 : {end_address}\n")
print("자동차")
print(f"- 거리 : {c_distance // 1000} km {c_distance % 1000} m")
print(f"- 시간 : {c_time//3600} h {c_time % 3600 // 60} min {c_time % 60} sec")
print(f"- 택시 요금 : {texi} KRW")
print(f"- 고속도로 통행료: {c_fare} KRW \n")
print(w_error)
if w_error == "도보":
    print(f"- 거리 : {w_distance // 1000} km {w_distance % 1000} m")
    print(f"- 시간 : {w_time//3600} h {w_time % 3600 // 60} min {w_time % 60} sec")
    print(f"- 소모칼로리: 약 {w_distance*0.05} kcal")
print("\n대중교통")
print(f"- 버스 경로수 : {bus_count}개")
print(f"- 지하철 경로수 : {sub_count}개")
print(f"- 버스 + 지하철 경로수 : {busub_count}개")
for i in range(3):
    c = 1
    for j in for_list[i]:
        print(f"\n{for_list_[i]} 경로 {c}")
        print(f"- 거리 : {j[2] // 1000} km {j[2] % 1000} m")
        print(f"- 시간 : {j[1] // 3600} h {j[1] % 3600 // 60} min {j[1] % 60} sec")
        print(f"- 비용 : {j[0]} KRW")
        print(f"- 추가 도보 거리 : {j[4] // 1000} km {j[4] % 1000} m")
        print(f"- 추가 도보 시간 : {j[3] // 3600} h {j[3] % 3600 // 60} min {j[3] % 60} sec")
        for k in range(5,len(j)):
            print(f"- [{'도보' if j[k][0] == 'WALK' else '버스' if j[k][0] == 'BUS' else '지하철'} {''if j[k][5] is None else j[k][5]}] {j[k][3]} -> {j[k][4]} | {j[k][1] // 3600} h {j[k][1] % 3600 // 60} min {j[k][1] % 60} sec | {j[k][2] // 1000} km {j[k][2] % 1000} m")
        c += 1
