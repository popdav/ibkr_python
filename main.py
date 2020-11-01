import ibapi
import time
import math

from ibapi.client import EClient
from ibapi.wrapper import EWrapper  
from ibapi.contract import Contract
from ibapi.order import *

import threading

class IBapi(EWrapper, EClient):
    
    def __init__(self):
        EClient.__init__(self, self) 
        self.current_bid_price = None
        self.current_ask_price = None
    def tickPrice(self, reqId, tickType, price, attrib):
        if tickType == 2 and reqId == 1:
            self.current_ask_price = price
            # print('The current ask price is: ', price)
        if tickType == 1 and reqId == 1:
            self.current_bid_price = price
            # print('The current bid price is: ', price)
    
    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextorderId = orderId
        print('The next valid order id is: ', self.nextorderId)
        
    def orderStatus(self, orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        print('orderStatus - orderid:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining, 'lastFillPrice', lastFillPrice)
	
    def openOrder(self, orderId, contract, order, orderState):
        print('openOrder id:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':', order.action, order.orderType, order.totalQuantity, orderState.status)
        
    def execDetails(self, reqId, contract, execution):
        print('Order Executed: ', reqId, contract.symbol, contract.secType, contract.currency, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)

def FX_order(symbol):
    contract = Contract()
    contract.symbol = symbol[:3]
    contract.secType = 'CASH'
    contract.exchange = 'IDEALPRO'
    contract.currency = symbol[3:]
    return contract

def set_order(typeAction, quantity, orderType, lmtPrice, finInstr):
    print(f'Setting order action:{typeAction}, quantity:{quantity}, price:{lmtPrice}')
    order = Order()
    order.action = typeAction
    order.totalQuantity = quantity
    order.orderType = orderType
    order.lmtPrice = lmtPrice
    order.orderId = app.nextorderId
    app.nextorderId += 1
    order.transmit = True
    
    app.placeOrder(order.orderId, finInstr, order)

def set_bracket_order(typeAction, quantity, orderType, lmtPrice, deltaProfit, finInstr):
    print(f'Setting order action:{typeAction}, quantity:{quantity}, price:{lmtPrice}')
    order = Order()
    order.action = typeAction
    order.totalQuantity = quantity
    order.orderType = orderType
    order.lmtPrice = lmtPrice
    order.orderId = app.nextorderId
    app.nextorderId += 1
    order.transmit = False

    takeProfit = Order()
    takeProfit.orderId = order.orderId + 1
    takeProfit.action = "SELL" if typeAction == "BUY" else "BUY"
    takeProfit.orderType = "LMT"
    takeProfit.totalQuantity = quantity
    takeProfit.lmtPrice = str(float(lmtPrice) + deltaProfit) if typeAction == "BUY" else str(float(lmtPrice) - deltaProfit) 
    takeProfit.parentId = order.orderId
    takeProfit.transmit = True
    
    app.placeOrder(order.orderId, finInstr, order)
    app.placeOrder(takeProfit.orderId, finInstr, takeProfit)
    


def run_loop():
	app.run()

app = IBapi()
app.connect('127.0.0.1', 7497, 123)

app.nextorderId = None

api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

while True:
    if isinstance(app.nextorderId, int):
        print('connected')
        break
    else:
        print('waiting for connection')
        time.sleep(1)

currentContract = FX_order('EURUSD')
app.reqMktData(1, currentContract, '', False, False, [])

while True:
    if app.current_bid_price is not None:
        break

price_to_buy = float(app.current_bid_price) * 1000000 / 10
last_digit = price_to_buy % 10
if last_digit >= 5:
    price_to_buy = math.floor(price_to_buy / 10) * 10 + 5
else:
    price_to_buy = math.floor(price_to_buy / 10) * 10
price_to_buy = price_to_buy / 100000
print(app.current_bid_price)
print(price_to_buy)
set_bracket_order('BUY', 20000, 'LMT', str(price_to_buy), 0.0001, currentContract)

app.disconnect()