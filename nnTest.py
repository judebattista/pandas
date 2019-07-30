import pandas as pd

sep = '+'*80

rep1 = [.6, .1, .1, .1, .1]
bb1 = [.8, .05, .05, .05, .05]
bbseq1 = [.9, .025, .025, .025, .025]
site1 = [rep1, bb1, bbseq1]
rep2 = [.1, .6, .1, .1, .1]
bb2 = [.05, .8, .05, .05, .05]
bbseq2 = [.025, .9, .025, .025, .025]
site2 = [rep2, bb2, bbseq2]
rep3 = [.1, .1, .6, .1, .1]
bb3 = [.05, .05, .8, .05, .05]
bbseq3 = [.025, .025, .9, .025, .025]
site3 = [rep3, bb3, bbseq3]

top = {
    1:site1,
    2:site2,
    3:site3
}

df = pd.DataFrame(top)
df2 = pd.DataFrame(data=top, index=['rep','bb','bbseq']) 
df3 = pd.DataFrame(data=top, index=['rep','bb','bbseq'], columns=['site1', 'site2', 'site3'] )
print(df.head())
print(df2.head())
print(df3.head())

print(sep)
print(df2[1].head())
print(df2.axes)

print(sep)
print(df2[1]['bb'])
#print(df2[:]['bb'])
