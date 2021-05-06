import pyupbit
import schedule
import time

access = "xMSuyEl4zzoRGxAfoCedxeYhhGFkag07MHlENBdq"          # 본인 값으로 변경
secret = "Jkw3HYoTDaR1YH3GNObMt6wujn2g7XauYq4xbovD"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

print(upbit.get_balance("KRW-BTC"))     # KRW-BTC 조회
print(upbit.get_balance("KRW"))            # 보유 현금 조회


def job(): # 아래 것을 주기적으로 실행
    a = upbit.get_balance("KRW") -5000
    b = upbit.get_balance("KRW-BTC") * pyupbit.get_current_price("KRW-BTC")
    c = upbit.get_balance("KRW-ETH") * pyupbit.get_current_price("KRW-ETH")
    d = upbit.get_balance("KRW-XRP") * pyupbit.get_current_price("KRW-XRP")
    e = upbit.get_balance("KRW-XRP") * pyupbit.get_current_price("KRW-DOGE")
    f = a + b + c + d + e
    
    if b/f < 0.35 :                                           # 참이려면 비트코인 가격이 하락하였을 때지
        upbit.buy_market_order("KRW-BTC", 0.35*e-b)     # 돈으로
    
    else :
        upbit.sell_market_order("KRW-BTC", (b-0.35*e)/pyupbit.get_current_price("KRW-BTC"))       # BTC로

    if c/f < 0.35 :                                           # 참이려면 비트코인 가격이 하락하였을 때지
        upbit.buy_market_order("KRW-ETH", 0.35*e-c)     # 돈으로
    
    else :
        upbit.sell_market_order("KRW-ETH", (c-0.35*e)/pyupbit.get_current_price("KRW-ETH"))       # ETH로

    if d/f < 0.3 :                                           # 참이려면 비트코인 가격이 하락하였을 때지
        upbit.buy_market_order("KRW-XRP", 0.15*e-d)     # 돈으로
    
    else :
        upbit.sell_market_order("KRW-XRP", (d-0.15*e)/pyupbit.get_current_price("KRW-XRP"))       # XRP로

    if e/f < 0.35 :                                           # 참이려면 비트코인 가격이 하락하였을 때지
        upbit.buy_market_order("KRW-BTC", 0.15*e-b)     # 돈으로
    
    else :
        upbit.sell_market_order("KRW-BTC", (b-0.15*e)/pyupbit.get_current_price("KRW-DOGE"))       # DOGE로
       # DOGE로

# schedule.every().hour.do(job)
# schedule.every(1).seconds.do(job)
# schedule.every(10).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every(5).to(10).minutes.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
schedule.every().minute.at(":00").do(job)
schedule.every().minute.at(":30").do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
