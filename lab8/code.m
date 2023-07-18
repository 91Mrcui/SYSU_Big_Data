% 读取文本文件
data = dlmread('email-Eu-core.txt');
data = data + 1;

% 顶点数
num_vertices = max(max(data));

% 稀疏矩阵
adj_matrix = sparse(data(:, 1), data(:, 2), 1, num_vertices, num_vertices);
adj_matrix = adj_matrix + adj_matrix.'; % 对称化，将其表示为无向图

% 计算模块化矩阵
gamma = 2; % 设置 gamma 值
%twom为网络图的加权边数的两倍
[modularity_matrix, twom] = modularity(adj_matrix, gamma);

% 读取真实的社区标签文件
ground_truth = dlmread('email-Eu-core-department-labels.txt');
ground_truth(:, 1:2) = ground_truth(:, 1:2) + 1;

% 调用genlouvain函数进行社区检测
[S, Q] = genlouvain(modularity_matrix,42);

% 计算NMI
nmi_value = compute_nmi(ground_truth(:, 2), S);

% 计算模块度
modularity_value = Q/twom;

% 显示结果
fprintf('community num: %d\n',max(S));
fprintf('NMI: %f\n', nmi_value);
fprintf('Modularity: %f\n', modularity_value);

% 将社区结果写入文本文件
fileID = fopen('community_results.txt', 'w');
fprintf(fileID, 'NodeID\tCommunityID\n');
for i = 1:length(S)
    fprintf(fileID, '%d\t%d\n', i, S(i));
end
fclose(fileID);