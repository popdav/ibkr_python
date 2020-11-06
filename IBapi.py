from ibapi.client import EClient
from ibapi.wrapper import EWrapper  


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
        # print('The next valid order id is: ', self.nextorderId)
        
    # def orderStatus(self, orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
    #     print('orderStatus - orderid:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining, 'lastFillPrice', lastFillPrice)
	
    # def openOrder(self, orderId, contract, order, orderState):
    #     print('openOrder id:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':', order.action, order.orderType, order.totalQuantity, orderState.status)
        
    # def execDetails(self, reqId, contract, execution):
    #     print(f'Order Executed: , {reqId}, {contract.symbol}, {contract.secType}, {contract.currency}, {execution.orderId}, {execution.shares}, {execution.lastLiquidity}')
