import pandas
import numpy
import random
from pathlib import Path
from math import *
from Equation import Expression

class Projection:
    def __init__(self, investment, percentage, txtName):
        self.investment = investment
        self.percentage = percentage
        self.txtName = txtName
        self.fieldNames = ['Users', 'Price', 'Economy', 'TVTNum', 'InvestorTVT', 'InvestorPerc', 'InvestorSell', 'InvestorReturn', 'InvestorPercReturn']
        txtFile = Path(txtName)
        if txtFile.is_file():
            self.projectionSnapshot()
        else:
            init = [[10000, 0.007, 270000000, 38000000000, 0, 0, 0, 0, -1]]
            self.df = pandas.DataFrame(init, columns=self.fieldNames)
            self.df.to_csv(txtName, index=False)

    def projectionSnapshot(self):
        self.df = pandas.read_csv(self.txtName)


    def add30Days(self, dailyEconomyFluctuation, growthRate):
        startingInfo = self.df.values[-1].tolist()
        totalSelloff = self.df['InvestorSell'].sum()
        print(startingInfo)
        userList = [startingInfo[0]]
        dailyList = [startingInfo]
        tokens = startingInfo[3]
        if growthRate == 0:
            for z in range(0,30):
                users = int(userList[-1])
                if users < 100000:
                    low = int(users*975/1000)
                elif users < 1000000 & users > 100000:
                    low = int(users*980/1000)
                elif users > 1000000:
                    low = int(users*985/1000)
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
            for z in range(0,30):
                users = userList[-1]
                fn = Expression(growthRate,["x"])
                userList.append(fn(users))

        newTokens = tokens
        for x in range(0, len(userList)):
            if x == 0:
                continue
            currentInfo = dailyList[-1]
            investorTokens = currentInfo[4]
            if userList[x] < 100000:
                newEcon = (userList[x] * 27000) + (random.randint(-1*dailyEconomyFluctuation-5,dailyEconomyFluctuation)*(userList[x] * 27000))/100
            else:
                newEcon = (userList[x] * 26000) + (random.randint(-1*dailyEconomyFluctuation-7,dailyEconomyFluctuation)*(userList[x] * 27000))/100
            newPrice = newEcon/tokens
            # Currently a reduction of 1% a day, this can be tuned by MV = PQ
            # Where PQ = Total Economy and Velocity is known
            # We now then can estimate how much free flowing TVT needs to exist
            # If there currently is a lot held by our "banks", they will have to release
            newInvestorTVT = investorTokens*99/100
            newInvestorPerc = currentInfo[4]*99/100
            newInvestorSelloff = (investorTokens - newInvestorTVT)*newPrice*0.95
            totalSelloff += newInvestorSelloff
            if x == 30:
                newTokens = int(newEcon/0.007)
                newInvestorTVT += int((self.percentage* (newTokens-tokens))/100)
                newInvestorPerc = newInvestorTVT/newTokens
                newPrice = 0.007
            newInvestorReturn = totalSelloff + newInvestorTVT * newPrice
            newInvestorPercReturn = newInvestorReturn/self.investment
            dailyList.append([userList[x], newPrice, newEcon, newTokens, newInvestorTVT, newInvestorPerc, newInvestorSelloff, newInvestorReturn, newInvestorPercReturn])

        del dailyList[0]
        df2 = pandas.DataFrame(dailyList, columns=self.fieldNames)
        self.df = self.df.append(df2, ignore_index=True, sort=False)
        print(self.df)
        self.df.to_csv(self.txtName, index=False)
