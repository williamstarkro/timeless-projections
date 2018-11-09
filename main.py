import pandas
from pathlib import Path
import numpy

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
            init = []
            init.append([10000, 0.007, 270000000, 38000000000, 0, 0, 0, 0, -1])
            self.df = pandas.DataFrame(init, columns=fieldnames)
            self.df.to_csv(txtName)

    def projectionSnapshot(self):
        self.df = pandas.read_csv(self.txtName)


    def add30Days(self, dailyEconomyFluctuation, growthRate):
        lst = []
        
