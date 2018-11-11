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
        self.investorReturn = 0
        self.txtName = txtName
        self.fieldNames = ['Users', 'Price', 'Economy', 'TVTNum', 'InvestorTVT', 'InvestorPerc', 'InvestorSell', 'InvestorReturn', 'InvestorPercReturn', 'Bond']
        self.bondTotal = 0
        txtFile = Path(txtName)
        if txtFile.is_file():
            self.projectionSnapshot()
        else:
            init = [[10000, 0.007, 270000000, 38000000000, 0, 0, 0, 0, -1, 0]]
            self.df = pandas.DataFrame(init, columns=self.fieldNames)
            self.df.to_csv(txtName, index=False)

    def projectionSnapshot(self):
        self.df = pandas.read_csv(self.txtName)

    def resetFile(self):
        open(self.txtName, 'w').close()
        init = [[10000, 0.007, 270000000, 38000000000, 0, 0, 0, 0, -1, 0]]
        self.df = pandas.DataFrame(init, columns=self.fieldNames)
        self.df.to_csv(self.txtName, index=False)

    def addSections(self, dailyEconomyFluctuation, growthRate, numberOfIncrements):
        for x in range(0,numberOfIncrements):
            self.add30Days(dailyEconomyFluctuation, growthRate)
    
    def deleteSections(self, numberOfIncrements):
        for x in range(0,numberOfIncrements):
            if len(self.df.index) > 30:
                self.df = self.df[:-30]

                openFile = open(self.txtName)
                lines = openFile.readlines()
                lines = lines[:-30]
                openFile.close()
                open(self.txtName, 'w').close()

                w = open(self.txtName,'w')
                w.writelines(lines)
                w.close()

    def changeShareOwnership(self, percentChange, investmentChange):
        if self.percentage + percentChange > 0 and self.percentage + percentChange < 100:
            self.percentage += percentChange
            if percentChange < 0:
                self.investorReturn += investmentChange
            else:
                self.investment += investmentChange


    def add30Days(self, dailyEconomyFluctuation, growthRate):
        startingInfo = self.df.values[-1].tolist()
        totalSelloff = self.df['InvestorSell'].sum()
        userList = [startingInfo[0]]
        dailyList = [startingInfo]
        tokens = startingInfo[3]
        if growthRate == 0:
            for z in range(0,30):
                users = int(userList[-1])
                if users < 100000:
                    low = int(users*975/1000)
                elif users < 1000000 and users > 100000:
                    low = int(users*980/1000)
                elif users > 1000000 and users < 10000000:
                    low = int(users*985/1000)
                elif users > 10000000:
                    low = int(users*995/1000)
                div = random.randint(low,users)
                exp = random.randint(1,3)
                sign = random.randint(1,100)
                if sign < 15 and users < 1000000:
                    sign = -1
                elif sign < 45 and users > 1000000:
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
        newBond = startingInfo[9]
        for x in range(0, len(userList)):
            if x == 0:
                continue
            currentInfo = dailyList[-1]
            investorTokens = currentInfo[4]

            # 27000/26000 is heuristic at this point
            # This is where UserValue.py will come into play
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
            newInvestorPerc = currentInfo[5]*99/100
            newInvestorSelloff = (investorTokens - newInvestorTVT)*newPrice*0.95
            totalSelloff += newInvestorSelloff
            if x == 30:
                newTokens = int(newEcon/0.007)
                newPrice = 0.007
                if newTokens > tokens:
                    nonBondTokens = (newTokens-tokens) - newBond 
                    if nonBondTokens < 0:
                        newBond = -1 * nonBondTokens
                        nonBondTokens = 0
                    else:
                        newBond = 0
                    newInvestorTVT += int((self.percentage * nonBondTokens)/100)
                    newInvestorPerc = newInvestorTVT/newTokens
                else:
                    newBond += (tokens - newTokens)
                
            newInvestorReturn = totalSelloff + newInvestorTVT * newPrice
            self.investorReturn = newInvestorReturn
            newInvestorPercReturn = (newInvestorReturn-self.investment)/self.investment
            dailyList.append([userList[x], newPrice, newEcon, newTokens, newInvestorTVT, newInvestorPerc, newInvestorSelloff, newInvestorReturn, newInvestorPercReturn, newBond])

        del dailyList[0]
        df2 = pandas.DataFrame(dailyList, columns=self.fieldNames)
        self.df = self.df.append(df2, ignore_index=True, sort=False)
        self.df.to_csv(self.txtName, index=False)
