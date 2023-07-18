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

# 设置Block-Stripe算法参数
block_size = 100
num_blocks = int(np.ceil(N/block_size))

# 初始化每个Block的稀疏矩阵
block_matrices = [None] * num_blocks
for i in range(num_blocks):
    block_indices = np.arange(i*block_size, min((i+1)*block_size, N))
    block_matrices[i] = np.zeros((len(block_indices), N))

# 将每个节点对应的数据加入对应Block的稀疏矩阵中
for i in range(N):
    block_idx = i // block_size
    row_idx = i % block_size
    block_start = indptr[i]
    block_end = indptr[i+1]
    block_indices = indices[block_start:block_end]
    block_data = weights[i] * data[block_start:block_end]
    block_matrices[block_idx][row_idx, block_indices] = block_data

print("calculating...\n")

# 计算PageRank值，迭代次数设置为500
for i in trange(100):
    pr_new = np.zeros(N)
    for j in range(num_blocks):
        block_indices = np.arange(j*block_size, min((j+1)*block_size, N))
        block_matrix = block_matrices[j]
        pr_new[block_indices] = (1 - d) / N + d * block_matrix.dot(pr)
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
