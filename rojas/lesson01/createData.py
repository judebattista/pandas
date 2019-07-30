from pandas import DataFrame, read_csv

import matplotlib   # to determine matplotlib version number
import matplotlib.pyplot as pt
import pandas as pd
import sys          # to determine Python version
import os

sep = '+++++++++++++++++++++++++++++++++++++++'

# enable matplotlib inline plotting
#%matplotlib inline

print('Python version: {0}'.format(sys.version))
print('Pandas version: {0}'.format(pd.__version__))
print('Matplotlib version: {0}'.format(matplotlib.__version__))

# create data
names = ['Bob','Jessica','Mary','John','Mel']
births = [968, 155, 77, 578, 973]

# create pairs using zip
babyDataSet = list(zip(names, births))
print('Baby data set: {0}'.format(babyDataSet))
print(sep)

# store the data in a dataframe (pandas object)
df = pd.DataFrame(data=babyDataSet, columns=['Names','Births'])
print(df)
print(sep)

# export to csv
df.to_csv('births1880.csv', index=False, header=False)

# read back from the csv
# note the r in front of the string which signifies a string literal
loc = r'./births1880.csv'
df2 = pd.read_csv(loc)
print(df2)
print(sep)

# Notice how df2 treat the first data item as the header
# We specified no header in our write function and read_csv defaults to assuming a header
df2 = pd.read_csv(loc, header=None)
print(df2)
print(sep)

# Now we have index values for column names
# We can specify a list of column names
df2 = pd.read_csv(loc, names=['Names','Births'])
print(df2)
print(sep)

# We are done with our CSV file and can remove it
os.remove(loc)

# Prepare the data:

# Investigate the data types
print('Column data types:\n{0}'.format(df.dtypes))
print(sep)
# We don't really care about the Names metadata since they're strings
# Pretty much anything goes there as long as it can be treated as a string
# We must be more careful with numeric data.
# note the plural/singular shift
print('Data type of births column:\n{0}'.format(df.Births.dtype))
# The int64 result guarantees all integer values

# Analyze the data:

# Method 1
sortedData = df.sort_values(['Births'], ascending=False)
print('The most common name in 1880 was:\n{0}'.format(sortedData.head(1)))

# Method 2
top = df['Births'].max()
print('The highest birthrate associated with a single name in 1880 was:\n{0}'.format(top))

# Displaying data
# Create the plot using the data in df
df['Births'].plot()
birthData = df['Births']
#maxVal = df['Births'].max()
maxVal = birthData.max()
#maxName = df['Names'][df['Births'] == df['Births'].max()].values
# The above line seems clumsy. Can we improve it with variables?
maxName = df['Names'][birthData == maxVal].values
maxText = str(maxVal) + ' - ' + maxName

# add text to graph
pt.annotate(maxText, xy=(1, maxVal), xytext=(8, 0), xycoords=('axes fraction', 'data'),
    textcoords='offset points')
print('The most popular name')
#print(df[df['Births'] == df['Births'].max()])
# Again, that seems clumsy, let's do it with variables
print(df[birthData == maxVal])

# At least from the CLI, pyplot requires an explicit command to show the plot
pt.show()

