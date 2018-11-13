#!/usr/bin/env python

import matplotlib.pyplot as plt

import pandas
df = pandas.read_csv('Timeless Projections.csv')


fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.plot(df['Day'], df['# of Users'], 'g-')
ax2.plot(df['Day'], df['Economy'], 'b-')

ax1.set_xlabel('Days')
ax1.set_ylabel('# of Users', color='g')
ax2.set_ylabel('Economy', color='b')

plt.show()
