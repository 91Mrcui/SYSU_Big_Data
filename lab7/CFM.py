import pandas as pd
import math
import numpy as np

# 读取训练集和测试集数据
train = pd.read_table('ml-100k/u1.base', sep='\t', header=None).iloc[:, :3].values
test = pd.read_table('ml-100k/u1.test', sep='\t', header=None).iloc[:, :3].values

n_users, n_items = 943+1, 1682+1    # 数据idx从1开始
n_samples = train.shape[0]

print(train.shape, test.shape)

glob_mean = np.mean(train[:, 2])    # 全局均分

# 创建用户物品评分矩阵
rating_matrix = np.zeros((n_users, n_items))
for i in range(n_samples):
    user = train[i, 0]
    item = train[i, 1]
    rating = train[i, 2]
    rating_matrix[user, item] = rating

# 预测函数
def predict(user, item):
    user_mean = np.mean(rating_matrix[user, :])
    item_mean = np.mean(rating_matrix[:, item])
    if user_mean == 0:
        user_mean = glob_mean
    if item_mean == 0:
        item_mean = glob_mean
    return (user_mean + item_mean) / 2

# 计算RMSE
sum_squared_error = 0
for i in range(test.shape[0]):
    user = test[i, 0]
    item = test[i, 1]
    actual_rating = test[i, 2]
    predicted_rating = predict(user, item)
    squared_error = (predicted_rating - actual_rating) ** 2
    sum_squared_error += squared_error

rmse = math.sqrt(sum_squared_error / test.shape[0])
print("RMSE:", rmse)
