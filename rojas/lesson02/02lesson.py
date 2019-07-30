import pandas as pd
from numpy import random
import matplotlib.pyplot as plt
import sys          # to determine python version number
import matplotlib   # to determine the matplotlib version number

# Would enable inline plotting were we in a Jupyter notebook
# %matplotlib inline

sep = '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'

print('Python version ' + sys.version)
print('Pandas version ' + pd.__version__)
print('Matplotlib version ' + matplotlib.__version__)

# The inital set of baby names
names = ['Bob','Jessica','Mary','John','Mel']

# Using the names list as source data, we will create a list of 1000 randomly chosen names
# Pick a specific seed so the experiment is repeatable
random.seed(500)
randNames = [names[random.randint(0, len(names))] for i in range(1000)]
#print(randNames[:10])

# Now let's generate random birth counts for each name in 1880
births = [random.randint(0, 1000) for i in range(1000)]

# Create pairs of name and birth data
babyDataSet = list(zip(randNames, births))
#print(babyDataSet[:10])

df = pd.DataFrame(data=babyDataSet, columns=['Names', 'Births'])
# Interestingly, this only shows 5 rows regardless of how large we make the end index
print(df[:10])

df.to_csv('births1880.csv', index=False, header=False)
loc = r'./births1880.csv'
df2 = pd.read_csv(loc)

print(sep)
print('Information about the imported csv file:')
print(df2.info())
print('Top of the data frame. Note the column names!')
print(df2.head())

# Let's reload the DF without headers
df2 = pd.read_csv(loc, header=None)

print(sep)
print('Information about the csv file when we import it without headers:')
print(df2.info())
print('Top of the data frame. Note the (lack of) column names!')
print(df2.head())

# What if we want to include column names, but don't want to use the first record in the DF 
# as the header info?
# Note that we now omit the header parameter
df2 = pd.read_csv(loc, names=['Names', 'Births'])
print(sep)
print('Top of the dataframe with explicitly named columns:')
print(df2.head(5))

# Because we constructed it, we know that there are five unique names in the DF
# How would we go about recovering them?
uniqueNames = df2['Names'].unique()
print(sep)
print('The unique names in the dataframe are: {0}'.format(uniqueNames))

# What if we want to aggregate the birth counts by name?
gbname = df2.groupby('Names')
df = gbname.sum()
print(sep)
print('Birth counts grouped by name:')
print(df)

# We can sort these values
byCount = df.sort_values(['Births'], ascending=False)
print(sep)
print('Data sorted by total birth counts per name')
print(byCount)
print('The most popular name was: ')
print(byCount.head(1))

# We can also get the max value directly:
maxCount = df['Births'].max()
print('The highest birth count was {0}.'.format(maxCount))

# Presenting the data:
df['Births'].plot.bar()
print(sep)
print('The most popular name:')
print(byCount)
plt.show()
