
# coding: utf-8

# # 기상 관측자료 크롤링

#     라이브러리 import 
#     1. request library : 파이썬에는 HTTP 요청을 처리할 수 있는 urllib이라는 모듈이 기본으로 들어 있으나 사용하기 불편함이 있다. 
#     최근에는 사용이 간편한 requests 모듈이 널리 사용되고 있다.
#     2. 웹 데이터 크롤링 또는 스크래핑을 할 때 사용하는 Python 라이브러리인 Beautiful Soup
# 

# In[96]:


import requests                  
from bs4 import BeautifulSoup   


#     3. 웹 페이지를 가져온 뒤 BeautifulSoup 객체로 만듦
# 

# In[97]:


response = requests.get('http://www.weather.go.kr/weather/observation/currentweather.jsp') # get 요청


# In[98]:


soup = BeautifulSoup(response.content, 'html.parser')


# In[99]:


soup


#     인터넷 창에서 fn + F12 누르면 HTML 창이 뜬다. 다음, 'ctrl + shif + c' 누르고 원하는 영역의 소스를 찾는다.
#     find 함수를 활용해 해당 부분의 내용만 불러온다.

# In[100]:


table = soup.find('table', { 'class': 'table_develop3'})


# In[101]:


table


# In[102]:


data = []                            # 데이터를 저장할 리스트 생성
for tr in table.find_all('tr'):      # 모든 <tr> 태그를 찾아서 반복(각 지점의 데이터를 가져옴)
    tds = list(tr.find_all('td'))    # 모든 <td> 태그를 찾아서 리스트로 만듦 (각 날씨 값을 리스트로 만듦)
    for td in tds:                   # <td> 태그 리스트 반복(각 날씨 값을 가져옴)
        if td.find('a'):             # <td> 안에 <a> 태그가 있으면(지점인지 확인)
            
            point = td.find('a').text # <a> 태그 안에서 지점을 가져옴
            yeonmoo = tds[1].text
            sijeong = tds[2].text
            woon = tds[3].text
            joong = tds[4].text
            temperature = tds[5].text    # <td> 태그 리스트의 여섯 번째(인덱스 5)에서 기온을 가져옴. 현재기온임ㅋㅋ
            isl = tds[6].text
            che = tds[7].text
            rain = tds[8].text
            humidity = tds[9].text       # <td> 태그 리스트의 열 번째(인덱스 9)에서 습도를 가져옴
            foong = tds[10].text
            wind = tds[11].text
            hpa = tds[12].text
            data.append([point, yeonmoo, sijeong, woon, joong, temperature, isl, che, rain, humidity, foong, wind, hpa])    # data 리스트에 지점, 기온, 습도를 추가


# In[103]:


point # for문 마지막 지점이 '남해'였나보네.


# In[104]:


data


#     추출한 리스트로 DataFrame 만들기

# In[105]:


import pandas as pd
data_df = pd.DataFrame(data)


# In[106]:


data_df.head()

# pd.DataFrame(df.values[:,1:], index=list(df[0]), columns=['기온', '습도'])


#     DataFrame 인덱싱 : df[0], 괄호 안은 컬럼명이다.

# In[107]:


data_df[0].head()


#     DataFrame 인덱싱 : df.loc[0], 괄호 안은 index 이름이다. / df.iloc[0], 괄호 안은 index 순서다.

# In[108]:


data_df.loc[0].head()


#     index = list(data_df[0]) vs index = data_df[0]

# In[109]:


data_df = pd.DataFrame(data = data_df.values[:,1:], index = list(data_df[0]), columns = ['현재일기','시정', '운량', '중하운량', '현재기온', '이슬점온도', '체감온도', '일강수', '습도', '풍향', '풍속', '기압' ])


# In[111]:


data_df.head()

