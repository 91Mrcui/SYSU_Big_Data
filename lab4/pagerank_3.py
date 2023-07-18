import numpy as np
from tqdm import trange

# 加载数据集
filename = 'Wiki-Vote.txt'
data = np.loadtxt(filename, dtype=int)

# 获取节点数量
N = np.max(data) + 1

# 统计每个节点的出度
out_degree = np.zeros(N)
for i, j in data:
    out_degree[i] += 1

# 计算每个节点对应的权重
weights = np.zeros(N)
for i in range(N):
    if out_degree[i] == 0:
        weights[i] = 1 / N
    else:
        weights[i] = 1 / out_degree[i]

# 初始化PageRank值
pr = np.ones(N) / N

# 阻尼系数
d = 0.85

# 构建稀疏矩阵
indices = data[:, 1]
indptr = np.zeros(N+1, dtype=int)
indptr[1:] = np.cumsum(out_degree)
data = np.ones(data.shape[0])
adj_matrix = np.zeros((N, N))
for i in range(N):
    block_start = indptr[i]
    block_end = indptr[i+1]
    block_indices = indices[block_start:block_end]
    block_data = weights[i] * data[block_start:block_end]
    adj_matrix[block_indices, i] = block_data

print("calculating...\n")

# 计算PageRank值，迭代次数设置为500
for i in trange(100): 
    pr_new = (1 - d) / N + d * adj_matrix.dot(pr)
    if np.allclose(pr, pr_new, atol=1e-6):
        break
    pr = pr_new

# 归一化处理
pr = pr / np.sum(pr)

# 输出结果
fp=open("result.txt",'w',encoding="utf-8")
for i, p in enumerate(pr):
    print(f'Node[{i}]: {p:.8f}')
    fp.write(f'Node[{i}]: {p:.8f}\n')
fp.close()
