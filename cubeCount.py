
####### deprecated  #######

import json
import requests
import pprint
from datetime import datetime, timedelta

def maple_API(user_name,target_item):
    ############ 큐브 api 관련 소스 ###########
    url = 'https://public.api.nexon.com/openapi/maplestory/v1/cube-use-results'
    key = apiToken.key[user_name]   #해당 키 부분은 따로 파일을 만들어서 입력해주세요. {캐릭터명:api key} 형태로 입력했습니다.
    
    ####### 장큡 명큡 레큡 블큡 #######
    j_cu = 0
    m_cu = 0
    r_cu = 0
    b_cu = 0
    
    ########시간 설정##########
    start = "2022-11-25"
    last = (datetime.today() - timedelta(days=1)).strftime(format="%Y-%m-%d")
    # last = "2022-11-26" #test용
    start_date = datetime.strptime(start, "%Y-%m-%d")
    last_date = datetime.strptime(last, "%Y-%m-%d")
    
    ###### api 조회 #########
    while start_date <= last_date:
        dates = start_date.strftime("%Y-%m-%d")
        print("날짜 :",dates)
        headers = {
            "authorization" : key
        }
        params = {
            "count" : 1000,
            "date" : dates,
            "cursor" : ""
        }
        res = requests.get(url,headers=headers,params=params)
        data = res.json()
        start_date += timedelta(days=1)
        if data['cube_histories'] == []:
            continue
        for c in range(data['count']):
            if data['cube_histories'][c]['character_name'] == user_name and data['cube_histories'][c]['target_item'] == target_item:
                if data['cube_histories'][c]['cube_type'] == '장인의 큐브':
                    j_cu = j_cu + 1
                if data['cube_histories'][c]['cube_type'] == '명장의 큐브':
                    m_cu = m_cu + 1
                if data['cube_histories'][c]['cube_type'] == '레드 큐브':
                    r_cu = r_cu + 1
                if data['cube_histories'][c]['cube_type'] == '블랙 큐브':
                    b_cu = b_cu + 1
                    
    return [j_cu,m_cu,r_cu,b_cu]