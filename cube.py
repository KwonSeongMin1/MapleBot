import requests
import apiToken #중요한 api key들 
import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('cube.db',isolation_level=None)
cursor = conn.cursor()

def update_cube_count(name,j_cu,m_cu,r_cu,b_cu):
    cursor.execute('update cubeCount set j_cu=?,m_cu=?,r_cu=?,b_cu=? where name=?;',(j_cu,m_cu,r_cu,b_cu,name))
    if cursor.rowcount > 0:
        return 1
    else:
        return 0 
    
def maple_API(name):
    ############ 큐브 api 관련 소스 ###########
    cursor.execute('select token from cubeCount where name = ?;',(name,))
    data = cursor.fetchone()
    if data is not None:
        token = data[0]  # 첫 번째 열의 값을 추출
        token_str = str(token)  # 문자열로 변환
        print(token_str)
    url = 'https://public.api.nexon.com/openapi/maplestory/v1/cube-use-results'
    key = token_str
    
    ######## 큐브 개수 ########
    j_cu = 0
    m_cu = 0
    r_cu = 0
    b_cu = 0
    ########시간 설정##########
    start = "2022-11-25"
    last = (datetime.today() - timedelta(days=1)).strftime(format="%Y-%m-%d")
    #last = "2022-11-26" #test용
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
            if data['cube_histories'][c]['character_name'] == name:
                if data['cube_histories'][c]['cube_type'] == '장인의 큐브':
                    j_cu = j_cu + 1
                if data['cube_histories'][c]['cube_type'] == '명장의 큐브':
                    m_cu = m_cu + 1
                if data['cube_histories'][c]['cube_type'] == '레드 큐브':
                    r_cu = r_cu + 1
                if data['cube_histories'][c]['cube_type'] == '블랙 큐브':
                    b_cu = b_cu + 1
                    
    update_cube_count(name,j_cu,m_cu,r_cu,b_cu)
    
def create_table(name,token):
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS cubeCount(
                       id INTEGER PRIMARY KEY,
                       name TEXT UNIQUE,
                       token TEXT,
                       j_cu INTEGER,
                       m_cu INTEGER,
                       r_cu INTEGER,
                       b_cu INTEGER
                   );
                   ''')
    try:
        cursor.execute('insert into cubeCount (name,token,j_cu,m_cu,r_cu,b_cu) values (?,?,?,?,?,?)',(name, token,0,0,0,0))
    except sqlite3.IntegrityError as e:
        print("이미 있는 닉네임입니다.")
        return 0

def cube_count(name):
    cursor.execute('select j_cu,m_cu,r_cu,b_cu from cubeCount where name=?',(name,))
    data = cursor.fetchone()
    return data
    
cube_count("순응하라")