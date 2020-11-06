from ibapi.contract import Contract
from ibapi.order import *

def FX_order(symbol):
    contract = Contract()
    contract.symbol = symbol[:3]
    contract.secType = 'CASH'
    contract.exchange = 'IDEALPRO'
    contract.currency = symbol[3:]
    return contract

def set_order(typeAction, quantity, orderType, lmtPrice, finInstr, app):
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

def set_order_profit_taker(typeAction, quantity, orderType, lmtPrice, deltaProfit, finInstr, app):
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
    takeProfit.orderId = app.nextorderId
    app.nextorderId += 1
    takeProfit.action = "SELL" if typeAction == "BUY" else "BUY"
    takeProfit.orderType = "LMT"
    takeProfit.totalQuantity = quantity
    takeProfit.lmtPrice = str(float(lmtPrice) + deltaProfit) if typeAction == "BUY" else str(float(lmtPrice) - deltaProfit) 
    takeProfit.parentId = order.orderId
    takeProfit.transmit = True
    
    app.placeOrder(order.orderId, finInstr, order)
    app.placeOrder(takeProfit.orderId, finInstr, takeProfit)

def set_order_stop_loss(typeAction, quantity, orderType, lmtPrice, deltaProfit, finInstr, app):
    print(f'Setting order action:{typeAction}, quantity:{quantity}, price:{lmtPrice}')
    order = Order()
    order.action = typeAction
    order.totalQuantity = quantity
    order.orderType = orderType
    order.lmtPrice = lmtPrice
    order.orderId = app.nextorderId
    app.nextorderId += 1
    order.transmit = False

    stopLoss = Order()
    stopLoss.orderId = order.orderId + 1
    stopLoss.action = "SELL" if typeAction == "BUY" else "BUY"
    stopLoss.orderType = "STP"
    stopLoss.totalQuantity = quantity
    stopLoss.auxPrice = str(float(lmtPrice) + deltaProfit) if typeAction == "BUY" else str(float(lmtPrice) - deltaProfit) 
    stopLoss.parentId = order.orderId
    stopLoss.transmit = True
    
    app.placeOrder(order.orderId, finInstr, order)
    app.placeOrder(stopLoss.orderId, finInstr, stopLoss)



def set_bracket_order(typeAction, quantity, orderType, lmtPrice, deltaProfit, finInstr, app):
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
    takeProfit.transmit = False

    stopLoss = Order()
    stopLoss.orderId = order.orderId + 2
    stopLoss.action = "SELL" if typeAction == "BUY" else "BUY"
    stopLoss.orderType = "STP"
    stopLoss.totalQuantity = quantity
    stopLoss.auxPrice = str(float(lmtPrice) + deltaProfit) if typeAction == "BUY" else str(float(lmtPrice) - deltaProfit) 
    stopLoss.parentId = order.orderId
    stopLoss.transmit = True
    
    app.placeOrder(order.orderId, finInstr, order)
    app.placeOrder(takeProfit.orderId, finInstr, takeProfit)
    app.placeOrder(stopLoss.orderId, finInstr, stopLoss)