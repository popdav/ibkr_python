import pandas as pd
import matplotlib.pyplot as plt
import math
from datetime import datetime

class Backtest:
    def __init__(self, balance, quantity, delta, df):
        self.balance = balance
        self.quantity = quantity
        self.delta = delta
        self.data = df
        self.current_taken_prices = []
        self.number_of_transaction = 0

    def calculate_current_buy_price(self, price):
        price_to_buy = float(price) * 1000000 / 10
        last_digit = price_to_buy % 10
        if last_digit >= 5:
            price_to_buy = math.ceil(price_to_buy / 10) * 10 
        else:
            price_to_buy = math.floor(price_to_buy / 10) * 10 + 5
        price_to_buy = price_to_buy / 100000

        return price_to_buy

    def buy(self, price):
        if price in self.current_taken_prices:
            return -1

        self.balance -= self.quantity * price
        self.number_of_transaction += 1
        self.current_taken_prices.append(price)
        print(f'Transaction: Buy, amount: {self.quantity}, price: {price}')

    def sell(self, price):
        self.balance += self.quantity * price
        self.number_of_transaction += 1
        self.current_taken_prices.remove((price - self.delta))
        print(f'Transaction: Sell, amount: {self.quantity}, price: {price}')

    def test(self):
        last = 0
        for index, row in self.data.iterrows():
            # if index == 10:
            #     break
            if len(self.current_taken_prices) == 0:
                price = self.calculate_current_buy_price(row['Open'])
                self.buy(price)
            
            reversed_list_prices = self.current_taken_prices[::-1]
            for level in reversed_list_prices:
                if float(row['High']) >= level + self.delta:
                    self.sell(level + self.delta)
                else:
                    break
            correct = 1
            # if len(self.current_taken_prices) > 15:
            #     correct = math.ceil(float(len(self.current_taken_prices))/15)

            if len(self.current_taken_prices) > 0 and float(row['Low']) <= self.current_taken_prices[-1] - correct * self.delta:
                self.buy(self.current_taken_prices[-1] - correct*self.delta)
                if float(row['Low']) <= self.current_taken_prices[-1] - 2*correct*self.delta:
                    self.buy(self.current_taken_prices[-1] - 2*correct*self.delta)

            last = float(row['High'])

        print(self.data.head())
        print(f'Balance: {self.balance}, Number of transactions: {self.number_of_transaction}, length of bought prices: {len(self.current_taken_prices)}')
        
        print(f'Total: {self.balance + len(self.current_taken_prices) * self.quantity * last}')

def main():
    

    data2018 = pd.read_csv('DAT_MT_EURUSD_M1_2018.csv')
    data2019 = pd.read_csv('DAT_MT_EURUSD_M1_2019.csv')
    frames = [data2018, data2019]
    data = pd.concat(frames)

    bt = Backtest(1000000, 50000, 0.0005, data)
    bt.test()

if __name__ == "__main__":
    main()