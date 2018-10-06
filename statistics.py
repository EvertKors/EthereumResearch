import sqlite3
from math import sqrt

conn = sqlite3.connect('new.db')
c = conn.cursor()

# Calculate average

# Get the value of ethereum transfered
data = c.execute("select value_eth from transactions where timestamp >= 1536638400 and timestamp <= 1536724800").fetchall()
value_list = [x[0] for x in data]
# Get the total of ether transfered
total = sum(value_list)
# Get the amount en data points
amount = float(len(value_list))
# Calculate average
mean = total / amount
print("Average:", mean)


# Calculate standard deviation
differences = [x - mean for x in value_list]
sq_differences = [d ** 2 for d in differences]
ssd = sum(sq_differences)
variance = ssd / amount
sd = sqrt(variance)
print('The standard deviation is ', sd)

