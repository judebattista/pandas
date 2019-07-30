import pandas as pd
import matplotlib.pyplot as plt
import numpy.random as np
import sys
import matplotlib
matplotlib.use('TkAgg')
sep = '+'*80

#%matplotlib inline
print('Python version ' + sys.version)
print('Pandas version: ' + pd.__version__)
print('Matplotlib version ' + matplotlib.__version__)

np.seed(111)
def CreateDataSet(Number=1):
    output = []

    for ndx in range(Number):
        # Create a data range
        dateRange = pd.date_range(start='1/1/2009', end='12/31/2012', freq='W-MON')
        length = len(dateRange)
        # Create random data
        data = np.randint(low=25, high=1000, size=length)

        # status pool
        status = [1, 2, 3]
        # Random list of statuses
        randStatus = [status[np.randint(low=0, high=len(status))] for i in range(length)]

        # state pool
        states = ['GA','FL','fl','NY','NJ','TX']
        # Random list of states
        randStates = [states[np.randint(low=0, high=len(states))] for i in range(length)]
        
        # merge the data and append to output
        output.extend(zip(randStates, randStatus, data, dateRange))
    return output

# Let's make some data!
dataset = CreateDataSet(4)
df = pd.DataFrame(data=dataset, columns=['State', 'Status', 'CustomerCount', 'StatusDate'])
print(df.info())
print(df.head())

# We can write this directly to an Excel file
# This does require installing the module openpyxl
df.to_excel('Lesson03.xlsx', index=False)
print('Done exporting to Excel')

print('Importing from Excel...')
loc = r'./Lesson03.xlsx'
# This in turn requires installation of the xlrd package
df = pd.read_excel(loc, 0, index_col='StatusDate')
print(df.dtypes)
print(df.index)
print(df.head())

# Prepare the data
# 1. Make sure the state name is in uppercase
# 2. Only select accounts with a status of 1
# 3. Marge NY and NJ to NY
# 4. Remove outliers

# 1. Uppercase
print(sep)
print('State names to uppercase')
# Look at our state values. Are any lowercase?
print(df['State'].unique())
# Yup, we have 'fl' in there
# Apply a lambda function to convert everything to uppercase
df['State'] = df['State'].apply(lambda x: x.upper())
# Did we get them all?
print(df['State'].unique())
# Yup, looks good

# 2. Status check
print(sep)
print('Only use accounts with a Status of 1')
print(df['Status'].unique())
mask = df['Status'] == 1
df = df[mask]
# Did we get them all?
print(df['Status'].unique())

# 3. State merge
print(sep)
print('Merging NY and NJ to NY.')
print(df['State'].unique())
mask = df['State'] == 'NJ'
df['State'][mask] = 'NY'
# Did we get them all?
print(df['State'].unique())

# 4. Outliers
print(sep)
# first plot the data to see what we're working with
df['CustomerCount'].plot(figsize=(15, 5))
plt.draw()
plt.close('all')

# The axis parameter determines whether we sort along rows or columns
#   It defaults to 0 (columns) so technically we don't need it here.
sortdf = df[df['State'] =='NY'].sort_index(axis=0)
print('New York accounts sorted by StatusDate')
print(sortdf.head(10))
# Notice the double entry for 2009-04-20 
# Now we want to compress the data to get daily customer counts per State and StatusDate
#   (We ignore Status since we have already filtered it to 1)
# The reset_index() method allows us to include the StatusDate in the calculation since we
#   previously designated it as an index, which is treated as distinct from a column
print('Summarized data grouped by State and StatusDate')
daily = df.reset_index().groupby(['State', 'StatusDate']).sum()
print(daily.head(10))

# Since the Status is always 1, we can remove it from the dataframe
del daily['Status']
print('After removing Status')
print(daily.head(10))

# After resetting the index and grouping the dataframe, what IS the index now?
print('After resetting the index and grouping the dataframe, we get the following index')
print(daily.index)
print('This index has multiple levels. The first is')
print(daily.index.levels[0])
print('The second is')
print(daily.index.levels[1])

# We can now plot the data by state
daily.loc['FL'].plot()
daily.loc['GA'].plot()
daily.loc['NY'].plot()
daily.loc['TX'].plot()
# The .draw() command will show any queued plots
plt.draw()
plt.close('all')

# We can further narrow our data set to a specific year, say 2012
daily.loc['FL']['2012':].plot()
daily.loc['GA']['2012':].plot()
daily.loc['NY']['2012':].plot()
daily.loc['TX']['2012':].plot()
plt.draw()
plt.close('all')

# The graphs indicate that the customer count is all over the place, which is reasonable since we 
#   randomly generated the values. What if we assume that the customer count should be relatively 
#   steady, as we might expect from a real-world data set?
# Then it becomes reasonable to exclude data points outside of a specific range
stYrMonth = daily.groupby([daily.index.get_level_values(0), 
    daily.index.get_level_values(1).year, daily.index.get_level_values(1).month])
# Create upper and lower bounds for outlierville
# We use transform instead of apply since transform retains the shape of our data 
#   while apply does not
# Since our data is not gaussian (based on previous graphs) we cannot use stats like μ and σ
#   instead we use percentiles to find outliers
daily['Lower'] = stYrMonth['CustomerCount'].transform(lambda x: x.quantile(q=.25) - 
    1.5*(x.quantile(q=.75) - x.quantile(q=.25)))
daily['Upper'] = stYrMonth['CustomerCount'].transform(lambda x: x.quantile(q=.75) + 
    1.5*(x.quantile(q=.75) - x.quantile(q=.25)))
# create a column to determine whether a record is an outlier or not
daily['Outlier'] = ((daily['CustomerCount'] < daily['Lower']) | 
    (daily['CustomerCount'] > daily['Upper']))
print('daily data with outlier info')
print(daily.head())
print(daily.info())
# Remove outliers
daily = daily[daily['Outlier'] == False]
print('After removing outliers')
print(daily.info())
# Interestingly, we only had one outlier
# What is daily at this point?
#   Customer counts aggregated by state and by day
#   Without outliers

# what if we want to get rid of the state distinctions?
gary = pd.DataFrame(daily['CustomerCount'].groupby(daily.index.get_level_values(1)).sum())
print(gary.head())
#gary.columns = ['CustomerCount'] # This doesn't seem to do anything...
#print(gary.head())

# group by year and month
yearMonth = gary.groupby([lambda x: x.year, lambda x: x.month])
print(yearMonth.head(10))
# Find max customer counts per year and month
gary['Max'] = yearMonth['CustomerCount'].transform(lambda x: x.max())
print(gary.head())

# What if we want to compare our data to goals?
# Thresholds for success for CustomerCounts
print(sep)
print('Comparison to annual goals')
data = [1000, 2000, 3000]
idx = pd.date_range(start='12/31/2011', end='12/31/2013', freq='A')
# big hairy annual goals
bhag = pd.DataFrame(data, index = idx, columns=['BHAG'])
print('Annual goals')
print(bhag)
# Recall that axis=0 means row-wise
comb = pd.concat([gary, bhag], axis=0)
comb = comb.sort_index(axis=0)
print('Combined data')
print(comb.tail())

fig, axes = plt.subplots(figsize=(12, 7))
comb['BHAG'].fillna(method='pad').plot(color='green', label='BHAG')
comb['Max'].plot(color='blue', label='All Markets')
plt.legend(loc='best')

print('Showing goal plot')
plt.draw()
plt.close('all')

# We can make predictions about next year's customer account too
# We will employ a simple algorithm using the percent change in the most recent year
# First we group our combined data by year
year = comb.groupby(lambda x: x.year).max()
print('The combined data grouped by year:')
print(year)

# Now add a column representing the percent change per year
year['PercentChange'] = year['Max'].pct_change(periods=1)
print('The combined data, grouped by year, with percent change from the previous year:')
print(year)

percentChange = 1 + year.loc[2012, 'PercentChange']
nextYear = year.loc[2012, 'Max'] * percentChange
print('The predicted count for 2013 is {0}.'.format(nextYear))

print(sep)
print('Plots by state')
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(20, 10))
fig.subplots_adjust(hspace=1.0)     # Create space between plots

daily.loc['FL']['CustomerCount']['2012':].fillna(method='pad').plot(ax=axes[0,0])
daily.loc['GA']['CustomerCount']['2012':].fillna(method='pad').plot(ax=axes[0,1]) 
daily.loc['TX']['CustomerCount']['2012':].fillna(method='pad').plot(ax=axes[1,0]) 
daily.loc['NY']['CustomerCount']['2012':].fillna(method='pad').plot(ax=axes[1,1]) 

# Add titles
axes[0,0].set_title('Florida')
axes[0,1].set_title('Georgia')
axes[1,0].set_title('Texas')
axes[1,1].set_title('North East');

plt.show()

