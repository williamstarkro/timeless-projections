import pandas
import numpy
import random
from pathlib import Path
from math import *
from Equation import Expression

"""
Spin up a Projection instance, letting you play around with investing into TVT Economy
We track the following information for every day:
    - Users (Service Providers)
    - Price of 1 TVT
    - Overall Economy Value
    - Number of TVT in existence
    - TVT holdings for the investor
    - % Ownership of TVT for the investor (% of all TVT in existence)
    - Daily selloff of TVT from the investor's holdings
    - Return (in terms of $) for the investor
    - % Return (in terms of initial investment) for the investor
    - Number of outstanding bonds
"""
class Projection:
    # Initializer for a Projection object
    # @Param _investment - Initial investment of capital to have TVT Share ownership
    # @Param _percentage - Initial percent ownership of TVT Share
    # @Param _txtName - Name of .txt file you want the data stored
    def __init__(self, _investment, _percentage, _txtName):
        # Store global variables
        self.investment = _investment
        self.percentage = _percentage
        self.investorShareReturn = 0
        self.txtName = _txtName
        self.fieldNames = ['Users', 'Price', 'Economy', 'TVTNum', 'InvestorTVT', 
            'InvestorPerc', 'InvestorSell', 'InvestorReturn', 'InvestorPercReturn', 'Bond']
        self.bondTotal = 0

        # Check if the txt file exists, if it does, we'll pull in the existing data
        # If it does not, we initialize the file and place in day 0 information
        txtFile = Path(self.txtName)
        if txtFile.is_file():
            self.projectionSnapshot()
        else:
            init = [[10000, 0.007, 270000000, 38000000000, 0, 0, 0, 0, -1, 0]]
            self.df = pandas.DataFrame(init, columns=self.fieldNames)
            self.df.to_csv(txtName, index=False)

    # Gather a snapshot of our txt file info and save it as a DataFrame
    def projectionSnapshot(self):
        self.df = pandas.read_csv(self.txtName)

    # Lets you restart the file and DataFrame from scratch
    def resetFile(self):
        open(self.txtName, 'w').close()
        init = [[10000, 0.007, 270000000, 38000000000, 0, 0, 0, 0, -1, 0]]
        self.df = pandas.DataFrame(init, columns=self.fieldNames)
        self.df.to_csv(self.txtName, index=False)

    # Add an n number of 30 day increments to our data
    # @Param _dailyEconomicFluctuation - Factor of how much the economy can move from the standard growth
    # @Param _growthRate - Increment/Decrement function of Users within the 30 days
    # Can be expressed either with your own math function (expressed as function of x), 
    # or use the built in method (input 0 is built in)
    # @Param _numberOfIncrements - Number of 30 day iterations 
    def addSections(self, _dailyEconomyFluctuation, _growthRate, _numberOfIncrements):
        for x in range(0, _numberOfIncrements):
            self.add30Days(_dailyEconomyFluctuation, _growthRate)
    
    # Lets you delete an n number of 30 day increments from the data
    # @Param _numberOfIncrements - Number of 30 day increments you want to delete
    def deleteSections(self, _numberOfIncrements):
        for x in range(0, _numberOfIncrements):
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

    # Allows you to change the percent ownership of shares you have
    # @Param _percentChange - Addition/subtraction from your total TVT ownership percentage
    # Expressed as a value (-100 to 100). 
    # @Param _investmentChange - Money either payed or recieved for the change in % ownership
    def changeShareOwnership(self, _percentChange, _investmentChange):
        # check that we are staying within the bounds of allowable percentages
        if self.percentage + _percentChange > 0 and self.percentage + _percentChange < 100:
            self.percentage += _percentChange
            # Decrease in % ownership is assumed to mean you sold it for money
            # This money goes to global investorShareReturn, which is an additive factor on investorReturn
            # Note that we do not decrease global investment variable, may need to be changed
            if _percentChange < 0:
                self.investorShareReturn += _investmentChange
            # Increase in % ownership is assumed to cost money
            # This money goes to global investment variable as an increase
            # Again, which variables are affected may need to be changed
            else:
                self.investment += _investmentChange


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
                
            newInvestorReturn = (totalSelloff + newInvestorTVT * newPrice) + self.investorShareReturn
            newInvestorPercReturn = (newInvestorReturn-self.investment)/self.investment
            dailyList.append([userList[x], newPrice, newEcon, newTokens, newInvestorTVT, newInvestorPerc, newInvestorSelloff, newInvestorReturn, newInvestorPercReturn, newBond])

        del dailyList[0]
        df2 = pandas.DataFrame(dailyList, columns=self.fieldNames)
        self.df = self.df.append(df2, ignore_index=True, sort=False)
        self.df.to_csv(self.txtName, index=False)
