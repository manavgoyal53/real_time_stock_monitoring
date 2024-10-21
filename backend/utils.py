import yfinance as yf
import json
from extensions import cache,mail,socketio
from flask_mail import Message
import datetime
from dateutil import tz

def get_stock_price(symbol):
    """
    Takes in the stock symbol and gives you the latest
    available day change in the price of that stock.
    First this logic would check for weekend days. Then
    for the market open close times and then for the active
    hours.
    """
    stock = yf.Ticker(symbol)
    tzlocal = tz.gettz("Asia/Kolkata")
    now = datetime.datetime.now().astimezone(tzlocal)
    date = now.date()
    weekday = date.isoweekday()
    open_time = datetime.datetime(day = date.day,month=date.month,year=date.year,hour=9,minute=15,tzinfo=tzlocal)
    close_time = datetime.datetime(day = date.day,month=date.month,year=date.year,hour=15,minute=30,tzinfo=tzlocal)
    market_close = (now > close_time and now > open_time) or (now < close_time and now < open_time)
    cached_data = cache.get(f"stock_{symbol}")

    if weekday in [6,7]:
        if not cached_data:
            diff = weekday - 5
            data = stock.history(interval="1m",start=date-datetime.timedelta(days=diff))
            data = json.loads(data["Close"].to_json(date_format="iso"))
            cache.set(f"stock_{symbol}",data)
            return data, False
        else:
            return cached_data, False
    elif market_close:    
        if not cached_data:
            if weekday == 1 and (now < close_time and now < open_time):
                data = stock.history(interval="1m",start=date-datetime.timedelta(days=3))
            else:
                data = stock.history(period='1d',interval="1m")
            data = json.loads(data["Close"].to_json(date_format="iso"))
            cache.set(f"stock_{symbol}",data)
            return data, False
        else:
            return cached_data,False
    else:
        if cached_data:
            data = stock.history(interval="1m",start=datetime.datetime.utcnow()-datetime.timedelta(minutes=1))
            new_data = {}
            new_data.update(cached_data)
            new_data.update(json.loads(data["Close"].to_json(date_format="iso")))
            cache.set(f"stock_{symbol}",new_data)
            return new_data, True
        else:
            data = stock.history(interval="1m",period="1d")
            data = json.loads(data["Close"].to_json(date_format="iso"))
            cache.set(f"stock_{symbol}",data)
            return data, True
            



def send_email_alert(user_email, stock_symbol, stock_price, threshold, alert_type):
    """
    Sends an email notification to the user when
    the price hits the specified threshold.
    """
    subject = f"Stock Alert: {stock_symbol}"
    body = f"The stock {stock_symbol} has reached your {alert_type} threshold of {threshold}. Current price: {stock_price}"

    msg = Message(subject=subject, recipients=[user_email], body=body)
    mail.send(msg)



def send_stock_data(stock_symbol):
    """
    This function runs for every minutes and emits 
    the data to the subscribed user using SocketIO.
    """
    stock = yf.Ticker(stock_symbol)
    data = stock.history(interval="1m",start=datetime.datetime.utcnow()-datetime.timedelta(minutes=1))
    new_data = {}
    cached_data = cache.get(f"stock_{stock_symbol}")
    new_data.update(cached_data)
    new_data.update(json.loads(data["Close"].to_json(date_format="iso")))
    cache.set(f"stock_{stock_symbol}",new_data,timeout=60*60*24)
    if not data.empty:
        timestamp = data.index[-1].isoformat()
        price = data['Close'].tail(1).item()
        socketio.emit('stock_update', {'timestamp': timestamp, 'price': price})