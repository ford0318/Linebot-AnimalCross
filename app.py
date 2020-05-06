# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

import os
import sys
from argparse import ArgumentParser
#from dotenv import load_dotenv, find_dotenv
import random
from getweather import weather
from currency_api import get_currencyjson
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    MemberJoinedEvent, MemberLeftEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton,
    ImageSendMessage)

import requests

app = Flask(__name__)
fish_price =[('吸盤魚','13000','海','北半球6-9月,南半球12-3月','全天'),
('鯨鯊','13000','海','北半球6-9月,南半球12-3月','全天'),
('鯊魚','15000','海','北半球6-9月,南半球12-3月','16-9點'),
('雙髻鯊','8000','海','北半球6-9月,南半球12-3月','16-9點'),
('鋸鯊','12000','海','北半球6-9月,南半球12-3月','16-9點'),
('魟魚','3000','海','北半球8-11月,南半球2-5月','4-21點'),
('翻車魚','4000','海','北半球7-9月,南半球1-3月','4-21點'),
('鬼頭刀','12000','碼頭','北半球5-10月,南半球11-4月','全天'),
('白面弄魚','4500','碼頭','北半球5-10月,南半球11-4月','全天'),
('鳳尾魚','200','海','南北半球全年','4-21點'),
('刺豚','2500','海','北半球7-9月,南半球1-3月','全天'),
('河豚','5000','海','北半球11-2月,南半球5-8月','21-4點'),
('獅子魚','500','海','北半球4-11月,南半球10-5月','全天'),
('蘇眉魚','10000','海','北半球7-8月,南半球1-2月','0-21點'),
('耳帶蝴蝶魚','1000','海','北半球4-9月,南半球10-3月','全天'),
('擬刺尾鯛','1000','海','北半球4-9月,南半球10-3月','全天'),
('孔雀魚','1300','河流','北半球4-11月,南半球10-5月','9-16點'),
('溫泉醫生魚','1500','河流','北半球5-9月,南半球11-3月','9-16點'),
('神仙魚','3000','河川','北半球5-10月,南半球11-4月','16-9點'),
('鬥魚','2500','河流','北半球5-10月,南半球11-4月','9-16點'),
('霓虹燈魚','500','河流','北半球4-11月,南半球10-5月','9-16點'),
('彩虹魚','800','河流','北半球5-10月,南半球11-4月','9-16點'),
('食人魚','2500','河流','北半球6-9月,南半球12-3月','21-4點、9-16點'),
('骨舌魚','10000','河流','北半球6-9月,南半球12-3月','16-9點'),
('黃金河虎','15000','河流','北半球6-9月,南半球12-3月','4-24點'),
('雀鱔','6000','水池','北半球6-9月,南半球12-3月','16-9點'),
('巨骨舌魚','10000','河流','北半球6-9月,南半球12-3月','16-9點'),
('恩氏多鰭魚','4000','河流','北半球6-9月,南半球12-3月','21-4點'),
('鱘魚','10000','河口','北半球9-3月,南半球3-9月','全天'),
('小丑魚','650','海','北半球4-9月,南半球10-3月','全天'),
('淡水龍蝦','200','水池','北半球4-9月,南半球10-3月','全天'),
('鱉','3750','河流','北半球8-9月,南半球2-3月','16-9點'),
('擬鱷龜','5000','河流','北半球4-10月,南半球10-4月','21-4點'),
('鯰魚','800','水池','北半球5-10月,南半球11-4月','16-9點'),
('遠東哲羅魚','15000','瀑布上','北半球12-3月,南半球6-9月','16-9點'),
('中華絲螯蟹','2000','河流','北半球9-11月,南半球3-5月','16-9點'),
('帝王鮭','1800','河口','北半球9月,南半球3月','全天'),
('鮭魚','700','河口','北半球9月,南半球3月','全天'),
('香魚','900','河流','北半球7-9月,南半球1-3月','全天'),
('櫻花鉤吻鮭','1000','瀑布上','北半球3-6月、9-11月,南半球3-5月、9-12月','16-9點'),
('花羔紅點鮭','3800','瀑布上','北半球3-6月、9-11月,南半球3-5月、9-12月','16-9點'),
('金鱒','15000','瀑布上','北半球3-6月、9-11月,南半球3-5月、9-11月','16-9點'),
('竹莢魚', '150','海','南北半球全年','全天'),
('鰈魚', '300','海','北半球10-4月,南半球4-10月','全天'),
('魷魚', '500','海','北半球12-8月,南半球6-2月','全天'),
('海馬','1100','海','北半球4-11月,南半球10-5月','全天'),
('海天使', '1000','海','北半球12-3月,南半球6-9月','全天'),
('燈籠魚', '2500','海','北半球11-3月,南半球5-9月','16-9點'),
('鯛魚', '3000','海','南北半球全年','全天'),
('條石鯛', '5000','海','北半球3-11月,南半球9-5月','全天'),
('皇帶魚', '9000','海','北半球12-5月,南半球6-11月','全天'),
('鱸魚', '400','海','南北半球全年','全天'),
('鮪魚', '7000','碼頭','北半球11-4月,南半球5-9月','全天'),
('矛尾魚', '15000','海','南北半球全年','下雨天'),
('比目魚', '800','海','南北半球全年','全天'),
('旗魚', '10000','碼頭','北半球7-9月、11-4月,南半球1-3月、5-10月','全天'),
('五彩鰻', '600','海','北半球6-10月,南半球12-4月','全天'),
('裸胸鱔','2000','海','北半球8-10月,南半球2-4月','全天'),
('太平洋桶眼魚', '15000','海','南北半球全年','21-4點'),
('西太公魚','400','河流','北半球12-2月,南半球6-8月','全天'),
('白斑狗魚','1800','河流','北半球9-12月,南半球3-6月','全天'),
('吳郭魚','800','河流','北半球6-10月,南半球12-4月','全天'),
('錦鯉','4000','水池','南北半球全年','16-9點'),
('鯉魚', '500','水池','南北半球全年','全天'),
('鯽魚', '160','河流','南北半球全年','全天'),
('紅目鯽', '900','河流','北半球11-3月,南半球5-9月','全天'),
('泥鰍', '400','河流','北半球3-5月,南半球9-11月','全天'),
('黑鱸魚', '400','河流','南北半球全年','全天'),
('黃鱸魚', '300','河流','北半球10-3月、南半球4-9月','全天'),
('鱧魚','5500','水池','北半球6-8月,南半球12-2月','9-16點'),
('藍鰓太陽魚', '180','河流','南北半球全年','9-16點'),
('金魚', '1300','水池','南北半球全年','全天'),
('蝌蚪', '100','水池','北半球3-7月,南半球9-1月','全天'),
('青蛙','120','水池','北半球5-8月,南半球11-2月','全天'),
('龍睛金魚', '1300','水池','南北半球全年','9-16點'),
('溪哥', '200','河流','南北半球全年','9-16點'),
('蘭壽金魚', '4500','水池','南北半球全年','9-16點'),
('珠星三塊魚', '240','河流','南北半球全年','16-9點'),
('塘鱧魚', '400','河流','南北半球全年','16-9點'),
('稻田魚','300','水池','北半球4-8月,南半球10-2月','全天')]

bugs_price = [('大藍閃蝶', '4000'),('椿象', '1000'),('飛蛾', '130'),('寄居蟹', '1000'),('海蟑螂', '200'),('狼蛛', '8000'),('虎甲蟲', '1500'),('星天牛', '350'),('蜜蜂', '200'),('蜈蚣', '600'),('蘭花螳螂', '2400'),('瓢蟲', '200'),('螳螂', '430'),('蓑衣蟲', '600'),('蝸牛', '250'),('鳳蝶', '240'),('白粉蝶', '160'),('斑緣點粉蝶', '160'),('鼠婦', '250')]

shell_price = [('珊瑚', '500'),('沙錢', '120'),('寶螺殼', '60'),('蛤蜊', '100'),('扇貝克', '900'),('海螺殼', '700'),('骨螺殼', '300'),('鐘螺殼', '180')]
 
other_price = [('自己島或者相同特產的島賣', '100'),('特產不相同的島賣', '500'),('椰子', '250'),('雜草', '10'),('春筍', '200'),('竹筍', '250'),('蜂巢', '300')]

#load_dotenv(find_dotenv())
#get channel_secret and channel_access_token from your environment variable

SECRET = os.environ.get('SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')

if SECRET is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if ACCESS_TOKEN is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)


line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(SECRET)

@app.route('/')
def index():
    return 'Hello!'

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    print("package_id:", event.message.package_id)
    print("sticker_id:", event.message.sticker_id)
    # ref. https://developers.line.me/media/messaging-api/sticker_list.pdf
    sticker_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 21, 100, 101, 102, 103, 104, 105, 106,
                   107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125,
                   126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 401, 402]
    index_id = random.randint(0, len(sticker_ids) - 1)
    sticker_id = str(sticker_ids[index_id])
    print(index_id)
    sticker_message = StickerSendMessage(
        package_id='1',
        sticker_id=sticker_id
    )
    line_bot_api.reply_message(
        event.reply_token,
        sticker_message)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """
    這裡很眼熟吧？就發送一個訊息
    quick_reply 底下的動作，就是幫你建立自動回覆的按鈕
    每一個 QuickReplyButton 都代表一個按鈕
    label 就是顯示的文字，text就是當你點下去，他會回復你的訊息
    最後一樣 push_message
    """
    # user_id = event.source.user_id
    text = event.message.text
    
    #line_bot_api.reply_message(event.reply_token, carousel_template_message)
    
    districts = ['嘉義縣','新北市','嘉義市','新竹縣', '新竹市', '臺北市', '臺南市', '宜蘭縣', '苗栗縣', '雲林縣', '花蓮縣', 
    '臺中市', '臺東縣', '桃園市', '南投縣', '高雄市', '金門縣', '屏東縣', '基隆市', '澎湖縣', '彰化縣', '連江縣']

    for a,b,c,d,e in fish_price:
        if event.message.text == a:
            text = f'{a}的價格: $ {b}\n出沒地點:{c}\n月份:{d}\n時間:{e}'
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text))
            return 0

    for a,b in bugs_price:
        if event.message.text == a:
            text = f'{a}的價格: $ {b}'
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text))
            return 0

    for a,b in shell_price:
        if event.message.text == a:
            text = f'{a}的價格: $ {b}'
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text))
            return 0

    for a,b in other_price:
        if event.message.text == a:
            text = f'{a}的價格: $ {b}'
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text))
            return 0
        
    
    fishlist=[]
    bugslist=[]
    shelllist=[]
    otherlist=[]

    #價格排序降序並把文字結果放在陣列
    def fish_text(fish_price):
        fish=[random.choice(fish_price) for i in range(6)]
        #fish = sorted(fish_price,key=lambda x:eval(x[1]),reverse=True)[:5]
        for a,b,c,d,e in fish:
            fishlist.append(f'{a}: $ {b}')

        return "\n".join(fishlist)

    def bugs_text(bugs_price):
        bugs=[random.choice(bugs_price) for i in range(6)]
        #bugs = sorted(bugs_price,key=lambda x:eval(x[1]),reverse=True)[:-10]
        for a,b in bugs:
            bugslist.append(f'{a}: $ {b}')

        return "\n".join(bugslist)

    def shell_text(shell_price):
    #shell=[random.choice(shell_price) for i in range(5)]
        shell = sorted(shell_price,key=lambda x:eval(x[1]),reverse=True)[:]
        for a,b in shell:
            shelllist.append(f'{a}: $ {b}')

        return "\n".join(shelllist)

    def other_text(other_price):
        other = sorted(other_price,key=lambda x:eval(x[1]),reverse=True)[:]
        for a,b in other:
            otherlist.append(f'{a}: $ {b}')

        return "\n".join(otherlist)
        
    if event.message.text =='Hi' or event.message.text =='嗨':
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text='請輸入:示範',
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                action=MessageAction(label="魚價格", 
                                text=fish_text(fish_price))
                            ),
                            QuickReplyButton(
                                action=MessageAction(label="蟲價格", 
                                text=bugs_text(bugs_price))
                            ),
                            QuickReplyButton(
                                action=MessageAction(label="貝殼價格", 
                                text=shell_text(shell_price))
                            ),
                            QuickReplyButton(
                                action=MessageAction(label="其他價格", 
                                text=other_text(other_price))
                            ),
                            QuickReplyButton(
                                action=MessageAction(label="天氣", 
                                text='臺北市')
                            )
                        ]
                    )
                )
        )
        return 0

    ## 天氣
    if '台' in text:
        text=text.replace('台','臺')
        if text in districts:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(weather(text)))
            return 0
    elif text in districts:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(weather(text)))
        return 0
    elif text == '示範':
        currency = get_currencyjson()
        currency_USDTWD = '更新時間: '+currency['USDTWD']['UTC']+'\n國際匯率: '+ format(currency['USDTWD']['Exrate'],'.4f')
        currency_USDJPY = '更新時間: '+currency['USDJPY']['UTC']+'\n國際匯率: '+ format(currency['USDJPY']['Exrate'],'.4f')
        currency_TWDJPY = '更新時間: '+currency['USDJPY']['UTC']+'\n國際匯率: '+ format(currency['USDTWD']['Exrate']/currency['USDJPY']['Exrate'],'.4f')
        wtcg=weather('臺中市')
        wtpe=weather('臺北市')

        line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
            alt_text='魚類名單',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://www.tech-girlz.com/wp-content/uploads/2020/04/%E5%8B%95%E6%A3%AE4%E6%9C%88%E9%AD%9A%E9%A1%9E-1024x680.png',
                        title='動物森友會查詢工具',
                        text='請依以下查詢教學操作',
                        actions=[
                            PostbackAction(
                                label='魚的價格',
                                data='fish'
                            ),
                            PostbackAction(
                                label='昆蟲價格',
                                data='bug'
                            ),PostbackAction(
                                label='其他價格',
                                data='other'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://www.tech-girlz.com/wp-content/uploads/2020/04/%E5%8B%95%E6%A3%AE4%E6%9C%88%E9%AD%9A%E9%A1%9E-1024x680.png',
                        title='匯率查詢工具',
                        text='請依以下查詢教學操作',
                        actions=[
                            MessageAction(
                                label='美金台幣',
                                text=currency_USDTWD
                            ),
                            MessageAction(
                                label='美金日幣',
                                text=currency_USDJPY
                            ),
                            MessageAction(
                                label='台幣日幣',
                                text=currency_TWDJPY
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://www.tech-girlz.com/wp-content/uploads/2020/04/%E5%8B%95%E6%A3%AE4%E6%9C%88%E9%AD%9A%E9%A1%9E-1024x680.png',
                        title='氣象查詢工具',
                        text='請依以下查詢教學操作',
                        actions=[
                            MessageAction(
                                label='台北市',
                                text=wtpe
                            ),
                            MessageAction(
                                label='台中市',
                                text=wtcg
                            ),
                            PostbackAction(
                                label='氣溫',
                                data='temperature'
                            )
                        ]
                    ),
                   
                ]
            )
        ))
        return 0
        
    elif text.isalnum():
        line_bot_api.reply_message(event.reply_token,TextSendMessage('請輸入:示範 獲得說明'))
        return 0

    
@handler.add(PostbackEvent)
def handle_postback(event):
    #postBack = event.postback.data
    if event.postback.data == 'fish':
        message = '請輸入魚類名稱'
    elif event.postback.data == 'bug':
        message = '請輸入昆蟲名稱'
    elif event.postback.data == 'other':
        message = '請輸入物品名稱'
    elif event.postback.data == 'rain':
        message = '請輸入縣市全名:如台中市'
    elif event.postback.data == 'temperature':
        message = '請輸入縣市全名:如台中市'
        
    message2 = TextSendMessage(text = message)
    line_bot_api.reply_message(event.reply_token, message2)
    
if __name__ == "__main__":
    # arg_parser = ArgumentParser(
    #     usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    # )
    # arg_parser.add_argument('-p', '--port', default=5000, help='port')
    # arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    # options = arg_parser.parse_args()

    # app.run(debug=options.debug, port=options.port)
    app.run()
