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
    # @Param _txtName - Name of .txt file you want the data stored (input as string)
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
    # Can be expressed either with your own math function (expressed as function of x in string format), 
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

    # Function to calculate daily user growth, then all other data points from user growth
    # @Param _dailyEconomicFluctuation - Factor of how much the economy can move from the standard growth
    # @Param _growthRate - Daily user growth rate
    def add30Days(self, _dailyEconomyFluctuation, _growthRate):
        # Pull in the last DataFrame row. Used as starting point for calculations
        startingInfo = self.df.values[-1].tolist()
        # Get the sum for all sell-offs of TVT, used in investorReturns variable
        totalSelloff = self.df['InvestorSell'].sum()
        # Array of Users for every day
        userList = [startingInfo[0]]
        # Array of all data points for every day
        dailyList = [startingInfo]

        # Built in function for increasing growth rate. Roughly logarithmic curve
        if _growthRate == 0:
            for z in range(0,30):
                # Get the last userCount in the array
                users = int(userList[-1])
                # Heuristic model of user growth, logarithmic. Does the following:
                #   - Finds a random number between low and "users" variable - div
                #   low = a percentage of "users" that gets closer to "users" value as "users" increases
                #   - Assigns a random exponent between 1 and 3 - exp
                #   - Computes a sign (-1 or 1) based on a random number between 1 and 100 - sign
                #   - Calculates newUsers by adding previous "users" to 
                #   sign * "users" * (1 - (users/div))^exp)
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
            # Calculation if you enter your own growth rate. 
            # Always should be in terms of x, inputted as a string
            fn = Expression(_growthRate,["x"])
            for z in range(0,30):
                users = userList[-1]
                userList.append(fn(users))

        # Calculation for all other data points per day
        # First pull current number of bonds and tokens
        prevTokens = startingInfo[3]
        newTokens = startingInfo[3]
        newBond = startingInfo[9]
        for x in range(0, len(userList)):
            # Skip over the first value, this was from the previous month
            if x == 0:
                continue
            # Get the previous day's information
            currentInfo = dailyList[-1]
            investorTokens = currentInfo[4]
            investorPerc = currentInfo[5]

            # Formula for calculating overall economy from daily users
            # Use the daily fluctuation to allow for variability in pricing
            # 27000/26000 is heuristic at this point
            # This is where UserValue.py will come into play
            if userList[x] < 100000:
                newEcon = (userList[x] * 27000) + (random.randint(-1* _dailyEconomyFluctuation-5, _dailyEconomyFluctuation)*(userList[x] * 27000))/100
            else:
                newEcon = (userList[x] * 26000) + (random.randint(-1* _dailyEconomyFluctuation-7, _dailyEconomyFluctuation)*(userList[x] * 27000))/100
            
            # TVT price is simply newEcon divided by total TVT outstanding
            newPrice = newEcon/prevTokens

            # Calculate investor TVT divestiture
            # Currently a reduction of 1% a day, this can be tuned by MV = PQ
            # Where PQ = Total Economy and Velocity is known
            # We now then can estimate how much free flowing TVT needs to exist
            # If there currently is a lot held by our "banks", they will have to release
            newInvestorTVT = investorTokens*99/100
            newInvestorPerc = investorPerc*99/100
            # Calculate value of the sell off (value * 0.95 to account for transaction costs/market movement)
            newInvestorSelloff = (investorTokens - newInvestorTVT)*newPrice*0.95
            totalSelloff += newInvestorSelloff

            # Monthly recalculation for # of TVT, so that each TVT = 0.007
            if x == 30:
                newTokens = int(newEcon/0.007)
                newPrice = 0.007
                # If # of TVT increases, this means no Bonds need to be created
                # First, all outstanding bonds need to be payed off,
                # Then any new TVT left over is spread out to TVT shareholders
                if newTokens > prevTokens:
                    nonBondTokens = (newTokens-prevTokens) - newBond 
                    if nonBondTokens < 0:
                        newBond = -1 * nonBondTokens
                        nonBondTokens = 0
                    else:
                        newBond = 0
                    newInvestorTVT += int((self.percentage * nonBondTokens)/100)
                    newInvestorPerc = newInvestorTVT/newTokens
                # If # of TVT goes down, then we have nothing to do but release new Bonds
                # Currently, assumed TVT decrease is coming from someone other than investor
                # Also, bond is converted at a 1:1 ratio, in reality bondholders would want a return
                else:
                    newBond += (prevTokens - newTokens)

            # Calculate investor return based off total selloff of TVT, current holdings of TVT, and any share selloffs they did    
            newInvestorReturn = (totalSelloff + newInvestorTVT * newPrice) + self.investorShareReturn
            newInvestorPercReturn = (newInvestorReturn-self.investment)/self.investment
            dailyList.append([userList[x], newPrice, newEcon, newTokens, newInvestorTVT, newInvestorPerc, newInvestorSelloff, 
                newInvestorReturn, newInvestorPercReturn, newBond])
        
        # Get rid of starting row in list of data
        del dailyList[0]
        # Update DataFrame and TXT file with new information
        df2 = pandas.DataFrame(dailyList, columns=self.fieldNames)
        self.df = self.df.append(df2, ignore_index=True, sort=False)
        self.df.to_csv(self.txtName, index=False)