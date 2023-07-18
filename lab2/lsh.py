import numpy as np
import random
from operator import itemgetter

# 桶的数量
num_buckets = 101
lsh_table = [[] for i in range(num_buckets)]

#计算两个向量之间的欧氏距离(l2-norm)
def l2_dist(x,y,r=2.0):
    dis=sum(((x[i] - y[i]) ** r) for i in range(len(x))) ** (1.0/r)
    return dis

#相似度
def cos_dist(x,y):
    prodAB = sum([x[i]*y[i] for i in range(len(x))])
    zeros = [0 for i in range(len(x))]
    A = l2_dist(x,zeros)
    B = l2_dist(y,zeros)
    return prodAB / (A*B)

# 哈希,str-->bucket id
def hash(sub_str):
    hash_value=sum([ord(c) for c in sub_str]) % num_buckets
    return hash_value

# minHash
def hash_minHash(x,var,cons,n):
    return (var*x + cons) % n

# 随机生成hash function
def get_hash_funs(n):
    hash_funcs = []
    for i in range(n):
        var = random.randint(0,1000)
        cons = random.randint(0,1000)
        hash_funcs.append([var,cons])
    return hash_funcs

def init_bucket(bands):
    array_buckets = []
    for band in range(bands):
        array_buckets.append([[] for i in range(num_buckets)])
    return array_buckets

# shingles --> row id
def init_matrix(docs,shingles):
    index = 0
    rows = {}
    for sh in shingles:
        for s in sh:
            if s not in rows:
                rows[s] = index
                index += 1
    return np.zeros((len(rows), len(docs))), rows

def shingles_hashed(shingles):
    shingles_hashed = []
    for substr in shingles:
        #对substr进行哈希
        key = hash(substr)
        shingles_hashed.append(key)
        lsh_table[key].append(substr)
    return shingles_hashed

def shingling(docment,k,h):
    docment = docment.lower()
    docment = ''.join(docment.split(' '))
    shingles = {}
    for i in range(len(docment)):
        substr = ''.join(docment[i:i+k])
        if len(substr) == k and substr not in shingles:
            shingles[substr] = 1
    if not h:
        return docment,shingles.keys()
    ret = tuple(shingles_hashed(shingles))
    return ret,ret

#选择一个k值，对每个文档构造k-shingle集合。
#h=True时将k-shingle哈希到较短的桶编号。
def construct_shingles_set(docs,k,h=False):
    shingles = []
    for i in range(len(docs)):
        doc = docs[i]
        doc,sh = shingling(doc,k,h)
        docs[i] = doc
        shingles.append(sh)
    return docs,shingles

#对文档-shingle对进行排序，按shingle排序。
def sort_document_shingles(docs,shingles):
    matrix,rows = init_matrix(docs,shingles)
    for col in range(len(docs)):
        for row in rows:
            if row in docs[col]:
                matrix[rows[row],col] = 1
    return matrix

#计算signature矩阵
def compute_minHash_signatures(matrix,n=12):
    hash_funcs = get_hash_funs(n)
    hash_value = []
    for func in hash_funcs:
        val = [hash_minHash(i,func[0],func[1],matrix.shape[0]) for i in range(matrix.shape[0])]
        hash_value.append(val)

    signature = np.zeros((n,matrix.shape[1])) + float('inf')

    for c in range(matrix.shape[1]):
        for r in range(matrix.shape[0]):
            if matrix[r,c] != 0:
                for i in range(n):
                    hi = hash_value[i]
                    signature[i,c] = min(signature[i,c],hi[r])
    return signature

# 找出相似的文本对(similarity > threshold),由于数据集的问题threshold选为0.65
def apply_LSH_technique(signature,threshold,bands=4,rows=3):
    init_buckets = init_bucket(bands)
    sim_pairs = {}
    i = 0
    for band in range(bands):
        buckets = init_buckets[band]        
        band = signature[i:i+rows,:]
        for col in range(band.shape[1]):
            key = int(sum(band[:,col]) % len(buckets))
            buckets[key].append(col)
        i = i+rows
        # 在每个桶中寻找相似文本对
        for item in buckets:
            if len(item) > 1:
                pair = (item[0], item[1])
                if pair not in sim_pairs:
                    x = signature[:,item[0]]
                    y = signature[:,item[1]]
                    similarity = cos_dist(x,y)
                    if(similarity >= threshold):
                        sim_pairs[pair] = similarity
    sort = sorted(sim_pairs.items(),key=itemgetter(1), reverse=True)
    return sort

if __name__ == '__main__':

    # 导入数据集
    with open('data.txt', encoding='utf-8') as file2:
        lines = file2.readlines()
    documents=[]
    for l in lines:
        l=l.replace('\n','')
        documents.append(l)

    k = 3 #length of shingles
    #1. get shingles set
    docschange,shingles = construct_shingles_set(documents[:],k)
    matrix = sort_document_shingles(docschange,shingles)
    #2. minhash get signatures
    signatures = compute_minHash_signatures(matrix,1000)
    #3. LSH require
    result = apply_LSH_technique(signatures,0.65,100,10)

    top_num = min(10,len(result))
    print(f'{top_num} most similar text pairs:\n')
    for i in range(top_num):
        pair = result[i][0]
        print(f"{i+1}. NO.{pair[0]} and NO.{pair[1]}, similarity:{result[i][1]}")
        print(documents[pair[0]]," <----> ",documents[pair[1]])
        print("")
        
    print(f"All pairs that similarity>0.65(totally {len(result)}):\n")
    for v in result:
        print(v[0],end=" ")
    print("\n")