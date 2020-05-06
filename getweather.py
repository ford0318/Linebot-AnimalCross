import requests
def weather(text):
    weatherlist=[]
    #名稱搜尋給結果
    #city_name = '嘉義縣'
    try:
        resp = requests.get('https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-2296F6EE-A99C-4170-AB81-9F8FF06DD307')
        weather_json = resp.json()
    except:
        return 'fail!'

    for i in weather_json:
    #sucess
    #result
    #records
        #print('-------------------')
    #準備剖析資料
        if i =='records':
            #剖析資料 'locationName'
            for i in weather_json['records']['location']:
                #print(i['locationName'])
                if i['locationName']== text:
                    title = text+'天氣:\n'
                    weatherlist.append(title)
                    element_wx = i['weatherElement'][0]['time']
                    element_pop = i['weatherElement'][1]['time']
                    element_mint = i['weatherElement'][2]['time']
                    element_mint = i['weatherElement'][4]['time']
                    
                    for i in range(3):
                        a=''.join([element_wx[i]['startTime'][5:-3],'到\n', element_wx[i]['endTime'][5:-3],'\n',element_wx[i]['parameter']['parameterName'],
                        '\n降雨機率:',element_pop[i]['parameter']['parameterName'],'%','\n最低溫:',element_mint[i]['parameter']['parameterName'],'C','\n最高溫:',element_mint[i]['parameter']['parameterName'],'C\n\n'])
                        weatherlist.append(a)
    return ''.join(weatherlist).rstrip()

if __name__ == '__main__':
    print(weather('臺中市'))
