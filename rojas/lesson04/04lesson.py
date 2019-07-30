import pandas as pd
import sys

# Character generator function
# Uses the Unicode values of characters provided by ord() to generate the range
# Then uses chr to convert each Unicode value back to a character
def charRange(c1, c2):
    for c in range(ord(c1), ord(c2)+1):
        yield chr(c)

print('Python version ' + sys.version)
print('Pandas version: ' + pd.__version__)

# initial small data set
d = [x for x in range(10)]

df = pd.DataFrame(d)
# Example of column manipulation
df.columns = ['Rev']
df['NewCol'] = 5
df['NewCol'] += 1
del df['NewCol']
#print(df)

df['test'] = 3
df['col'] = df['Rev']
#print(df)

# renaming the index:
ndx = charRange('a','j')
df.index = ndx
print(df)

print(df.loc['a'])
