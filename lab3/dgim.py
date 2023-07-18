import random
import math


def write_to_file(filename,list):
    fp=open(filename,'w',encoding='utf-8')
    for i in range(len(list)):
        fp.write(str(list[i]))
        if i%100==0 and i!=0:
            fp.write('\n')
    fp.close()

class DGIM:
    def __init__(self, windowsize):
        self.windowsize=windowsize # window
        self.keysnum=int(math.log(self.windowsize,2))+1 
        self.keylist=[]
        self.buckets = {}  
        self.timestamp = 0  # init time stamp
        self.updatestep = windowsize  # updatestep <= windowsize
        self.updateidx = 0  
        # init
        for i in range(self.keysnum):
            key=int(math.pow(2,i))
            self.buckets[key]=[]
            self.keylist.append(key)

    # update function
    def update(self):
        for key in self.keylist:
            if len(self.buckets[key])>2:
                self.buckets[key].pop(0)
                time_stamp=self.buckets[key].pop(0)
                if key!=self.keylist[-1]:
                    self.buckets[key*2].append(time_stamp)
            else:
                break
    
    # Counting the number of 1s in the last windows
    def count(self):
        nums=0
        first_stamp=0
        for key in self.keylist:
            if (len(self.buckets[key])>0):
                first_stamp=self.buckets[key][0]
        for key in self.keylist:
            for stamp in self.buckets[key]:
                if (stamp!=first_stamp):
                    nums+=key
                else:
                    nums+=0.5*key
        return nums
    
    # add a bit
    def add(self,var):
        self.timestamp=(self.timestamp+1) % self.windowsize
        for key in self.buckets.keys():
            for tstamp in self.buckets[key]:
                if self.timestamp == tstamp:
                    self.buckets[key].remove(tstamp)
        if var==1:
            self.buckets[1].append(self.timestamp)
            self.update()
        self.updateidx=(self.updateidx+1)%self.updatestep
        if self.updateidx==0:
            self.count()


if __name__=="__main__":
    LENGTH=1000000
    # Generate the bit stream
    stream = [random.randint(0, 1) for _ in range(LENGTH)]
    write_to_file('stream.txt',stream)

    # 1. Sampling a fixed proportion (10%) of the stream:
    sample_fix_proportion=[]
    for bit in stream:
        p=random.random()
        if p<0.1:
            sample_fix_proportion.append(bit)
    write_to_file('sampled_fix_proportion.txt',sample_fix_proportion)


    # 2. Sampling a fixed-size sample (1,000)
    sample_fix_size=[]
    SIZE=1000
    probability=float(SIZE)/float(LENGTH)
    for bit in stream:
        p=random.random()
        # discard it
        if p>probability:
            continue
        if len(sample_fix_size)<SIZE:
            sample_fix_size.append(bit)
        else:
            choose=random.randint(0,SIZE-1)
            sample_fix_size.pop(choose)
            sample_fix_size.append(bit)
    write_to_file('sampled_fix_size.txt',sample_fix_size)


    #3. Counting the number of 1s in the last N elements (N=50,000)
    dgim = DGIM(50000)
    for bit in stream:
        dgim.add(bit)
    res=int(dgim.count())
    real=sum(stream[1000000-50000:1000000])
    print("Number of 1s in the original stream: ", sum(stream))
    print("Number of 1s in the sample(fixed proportion): ", sum(sample_fix_proportion))
    print("Number of 1s in the sample(fix size): ", sum(sample_fix_size))
    print("Number of 1s in the last 50000 bits: ",res)
    print("Real number of 1s in the last 50000 bits:: ", real)
    print(f"Error:{100*float(abs(real-res))/float(real)}%")
    
