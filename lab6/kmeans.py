import numpy as np
# 调库取得uci数据集
from sklearn import datasets  
from sklearn import metrics

#kmeans算法
def kmeans(X, n_clusters, max_iterations=10000):
    # 初始化聚类中心
    centroids = X[np.random.choice(range(X.shape[0]), size=n_clusters, replace=False)]
    
    for _ in range(max_iterations):
        # 分配样本到最近的聚类中心
        labels = assign_labels(X, centroids)
        # 更新聚类中心
        new_centroids = update_centroids(X, labels, n_clusters)
        # 检查聚类中心是否收敛
        if np.allclose(centroids, new_centroids):
            break
        centroids = new_centroids
    return labels

def assign_labels(X, centroids):
    distances = np.linalg.norm(X[:, np.newaxis] - centroids, axis=-1)
    return np.argmin(distances, axis=-1)

def update_centroids(X, labels, n_clusters):
    centroids = np.zeros((n_clusters, X.shape[1]))
    for k in range(n_clusters):
        centroids[k] = np.mean(X[labels == k], axis=0)
    return centroids

data = datasets.load_iris()
#data = datasets.load_breast_cancer()

X = data.data
y_true = data.target

# 聚类数目
n_clusters = 3

# 运行K-means聚类算法
labels = kmeans(X, n_clusters)

# 输出聚类结果
print(labels)
print(y_true)

# 计算NMI
result_NMI=metrics.normalized_mutual_info_score(labels, y_true)
print("Normalized Mutual Information (NMI):", result_NMI)