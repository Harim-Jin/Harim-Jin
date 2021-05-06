import time
import pyupbit
import datetime
import requests
import json


access = "go2Bjby3VE4tXv06MLNp9uyn1i9xxFxmtMU7kTYT"
secret = "QA8XqaxJKPtgDdgLBIeFSbQfX3tkPMiogqvYmh1n"
myToken = ""
slack_webhook_url = "https://hooks.slack.com/services/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"


def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )
    
    
def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_ma15(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15

def get_balance(coin):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == coin:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
# 시작 메세지 슬랙 전송
post_message((myToken,"#jcoin", "리플 자동매매 시작!")

while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-XRP")
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-XRP", 0.4)
            ma15 = get_ma15("KRW-XRP")
            current_price = get_current_price("KRW-XRP")
            if target_price < current_price and ma15 < current_price:
                krw = get_balance("XRP")
                if krw > 5000:
                    buy_result = upbit.buy_market_order("KRW-XRP", ( krw*0.9995)*0.25)
                    post_message(myToken,"#bit", "XRP buy : " +str(buy_result))
        else:
            xrp = get_balance("XRP")
            currnt_price = get_current_price("KWR-XRP")
            avg = upbit.avg_buy_price("KWR-XRP")
                if xrp > 0.000073 or avg + (avg*0.2) < current_price:
                    sell_result = upbit.sell_market_order("KRW-XRP", xrp*0.9995)
                    post_message(myToken,"#bit", "XRP sell : " +str(sell_result))
        time.sleep(1)             

    except Exception as e:
        print(e)
        post_message(myToken,"#jcoin", "XRP Error")
        time.sleep(1)
