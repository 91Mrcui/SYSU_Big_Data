import numpy as np
from tqdm import trange
# 加载数据集
filename = 'Wiki-Vote.txt'
data = np.loadtxt(filename, dtype=int)

# 构建邻接矩阵
N = np.max(data) + 1
adj_matrix = np.zeros((N, N))
for i, j in data:
    adj_matrix[j, i] = 1

# 初始化PageRank值
pr = np.ones(N) / N

# 阻尼系数
d = 0.85
print("caculating...\n")
# 计算PageRank值，迭代次数设置为500
for i in trange(500): 
    pr_new = np.zeros(N)
    for j in range(N):
        pr_new[j] = (1 - d) / N + d * np.sum(pr * adj_matrix[:, j])
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
