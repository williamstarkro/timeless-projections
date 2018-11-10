import pandas
import numpy
import random
from pathlib import Path
from math import *

class Projection:
    def __init__(self, investment, percentage, buyinValue, txtName):
        self.investment = investment
        self.percentage = percentage
        self.buyinValue = buyinValue
        self.txtName = txtName
        txtFile = Path(txtName)
        if txtFile.is_file():
            self.projectionSnapshot()
        else:
            fieldnames = ['Users', 'Price', 'Economy', 'TVTNum', 'InvestorTVT', 'Investor%', 'InvestorSell', 'InvestorReturn', 'Investor%Return']
            init = [[10000, 0.007, 270000000, 38000000000, 0, 0, 0, 0, -1]]
            self.df = pandas.DataFrame(init, columns=fieldnames)
            self.df.to_csv(txtName)

    def projectionSnapshot(self):
        self.df = pandas.read_csv(self.txtName)


    def add30Days(self, dailyEconomyFluctuation, growthRate):
        startingInfo = self.df.values[-1].tolist()
        userList = [startingInfo[1]]
        print(userList[0])
        dailyList = []
        tokens = self.df.tail(1)['TVTNum']
        if growthRate == 0:
            for x in range(0,30):
                users = userList[-1]
                low = int(users*975/1000)
                div = random.randint(low,users)
                exp = random.randint(1,3)
                sign = random.randint(1,100)
                if sign < 15:
                    sign = -1
                else:
                    sign = 1
                newUsers = users + sign*(int(users * (((users/div)**exp)-1)))
                userList.append(newUsers)
        else:
            code = """
            ef g(x):
                return %s
            """ % growthRate

            for x in range(0,30):
                users = userList[-1]
                newUsers = exec(code)
                userList.append(newUsers)
        print(userList)
        '''
        for x in range(0, len(userList)):
            if x == 0:
                continue
            currentInfo = dailyList[-1]
            investorTokens = dailyList[-1][3]
            if userList[x] < 100000:
                    newEcon = userList[x] * (27000 * random.randint(-1*dailyEconomyFluctuation,dailyEconomyFluctuation))/110
                elif x < 1000000:
                    newEcon = userList[x] * (26000 * random.randint(-1*dailyEconomyFluctuation,dailyEconomyFluctuation))/115
                newPrice = newEcon/tokens
                newInvestorTVT = investorTokens*99/100
                newInvestor% = currentInfo['Investor%']*99/100
                if investorTokens < newInvestorTVT:
                    newInvestorSelloff = 0
                else:
                    newInvestorSelloff = (investorTokens - newInvestorTVT)*
                dailyList.append([userList[x], newPrice, newEcon, newInvestorTVT, newInvestor%, ])
        '''
