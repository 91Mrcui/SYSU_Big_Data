import pandas as pd
import math
import numpy as np
from matplotlib import pyplot as plt
dlist=[]
# 读取训练集和测试集数据
train_data = pd.read_table('ml-100k/u1.base', sep='\t', header=None).iloc[:, :3].values
test_data = pd.read_table('ml-100k/u1.base', sep='\t', header=None).iloc[:, :3].values

# 用户数量和物品数量（索引从1开始）
users_num, items_num = 944, 1683

# 样本数量
samples_num = train_data.shape[0]

print(train_data.shape, test_data.shape)

# 隐因子的数量
k = 20

# 全局均值
mean_arr = np.mean(train_data[:, 2])

# 物品和用户的偏置项
b_item = np.random.randn(items_num)
b_user = np.random.randn(users_num)

# 物品和用户的隐因子矩阵
qi = np.random.randn(items_num, k)
pu = np.random.randn(users_num, k)

# 用于快速查询物品和用户的字典
item_to_user = dict()
user_to_item = dict()

# 训练
max_iteration = 50  # 最大迭代次数
learning_rate = 0.01  # 学习率
alpha = 0.1  # 正则化项系数

for epoch in range(max_iteration):
    MSE = 0
    index = np.random.permutation(samples_num)

    for idx in index:
        user_id, item_id, rating = train_data[idx]

        # 预测评分
        y_pred = mean_arr + b_item[item_id] + b_user[user_id] + np.dot(pu[user_id], qi[item_id].T)
        err = rating - y_pred
        MSE += err**2

        # 更新偏置项和隐因子矩阵
        b_user[user_id] += learning_rate * (err - alpha * b_user[user_id])
        b_item[item_id] += learning_rate * (err - alpha * b_item[item_id])
        temp = qi[item_id]
        qi[item_id] += learning_rate * (err * pu[user_id] - alpha * qi[item_id])
        pu[user_id] += learning_rate * (err * temp - alpha * pu[user_id])

    MSE /= samples_num
    RMSE = math.sqrt(MSE)
    print("epoch:", epoch+1, "train_data RMSE:", RMSE)
    dlist.append(RMSE)

Y_pred = list()
test_data_mse = 0

# 测试误差
for sample in test_data:
    user_id, item_id, rating = sample
    y_pred = mean_arr + b_item[item_id] + b_user[user_id] + np.dot(pu[user_id], qi[item_id].T)
    test_data_mse += (rating - y_pred)**2

test_data_mse /= len(test_data)
test_data_rmse = math.sqrt(test_data_mse)

print("test_data RMSE: ", test_data_rmse)
plt.plot(dlist)
plt.show()