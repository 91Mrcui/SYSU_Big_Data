import csv
import pandas as pd
from apyori import apriori
import time


# read
with open('data.csv', 'r') as file:
    transactions = list(csv.reader(file))
 

min_supp = 0.4  
min_conf = 0.5  
min_lift = 0.1  
time_start = time.time() #开始计时
# apriori method
ap = list(apriori(transactions=transactions, min_support=min_supp, 
           min_confidence=min_conf, min_lift=min_lift))  

time_end = time.time() 
#support
supports=[]
confidences=[]
lifts=[]
# items_base
bases=[]
# items_add
adds=[]
 
for r in ap:
    for x in r.ordered_statistics:
        supports.append(r.support)
        confidences.append(x.confidence)
        lifts.append(x.lift)
        bases.append(list(x.items_base))
        adds.append(list(x.items_add))

output=[]
for i in range(len(confidences)):
    if(bases[i]!=[]):
        output.append([bases[i],adds[i],confidences[i],supports[i]])

output=sorted(output,key=lambda x:-x[2])


print('\n==High-confidence association rules (min_conf='+str(min_conf*100)+'%)\n')

for v in output:
    print('['+v[0][0]+']'+" => "+'['+v[1][0]+'] '+'(Conf: '+str(100*v[2])+'%, Supp: '+str(100*v[3])+'%)')  

print(f"\nusing time: {1000*(time_end-time_start):.4f} ms")