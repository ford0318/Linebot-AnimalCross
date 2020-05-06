import requests

url = 'https://tw.rter.info/capi.php' 

def get_currencyjson():
    r=requests.get(url)
    currency=r.json()
    return currency

if __name__ == '__main__':
    get_currencyjson()
    current_message =['更新時間: ',currency['USDTWD']['UTC'],'\n國際匯率: ',currency['USDTWD']['Exrate']]