import mapper
import reducer
import threading

word_map=[]
n=3
for i in range(n):
    word_map.append([])

# sorts and shuffles function
def Sorts_and_Shuffles(map_res):
    map_res.sort()
    return map_res
    
def main():
    filename = ['input\input_1.txt','input\input_2.txt','input\input_3.txt']
    threads = []
    # using Multi-threading, each thread is a mapper, simulating parallel situations
    for i in range(n):
        thread = threading.Thread(target= mapper.map,args=(filename[i],word_map[i],i))
        thread.start()
        threads.append(thread) 
    for thread in threads:
        thread.join()
    
    # Record the output of each mapper, and write to output_1.txt
    output1=open('output\output_1.txt','w',encoding='utf-8')
    print(len(word_map))
    for i in range(len(word_map)):
        output1.write("################################################################\n"+
        "The result of Map "+str(i)+"\n################################################################\n")
        for var in word_map[i]:
            output1.write('('+var+',1)\n')
    output1.close()

    # sorts and shuffles the output of each mapper, the record the result in output_2.txt
    output2= open('output\output_2.txt', 'w',encoding='utf-8') 
    for i in range(n):
        word_map[i]=Sorts_and_Shuffles(word_map[i])
        output2.write("################################################################\n"+
        "Sorts and shuffles of Map "+str(i)+"\n################################################################\n")
        for v in word_map[i]:
            output2.write('('+v+',1)\n')
    output2.close()

    # reduce
    word_reduced = reducer.reduce(word_map)

    #Write the result of reduce to output_3.txt
    f= open('output\output_3.txt', 'w',encoding='utf-8')
    f.write('The finnal result of mapreduce:\n') 
    for item in word_reduced.items():
        print(item)
        for i in range(len(item)):
            f.write(str(item[i])+' ')
        f.write('\n') 

if __name__ == '__main__':
    main()
