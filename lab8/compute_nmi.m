function nmi_value = compute_nmi(labels_true, labels_pred)
    % 计算 NMI
    n = length(labels_true);
    
    % 计算真实标签的熵
    unique_labels_true = unique(labels_true);
    p_true = histcounts(labels_true, unique_labels_true) / n;
    h_true = -sum(p_true .* log2(p_true));
    
    % 计算预测标签的熵
    unique_labels_pred = unique(labels_pred);
    p_pred = histcounts(labels_pred, unique_labels_pred) / n;
    h_pred = -sum(p_pred .* log2(p_pred));
    
    % 计算互信息
    labels_joint = [labels_true, labels_pred];
    p_joint = histcounts2(labels_joint(:,1), labels_joint(:,2), ...
        unique_labels_true, unique_labels_pred) / n;
    h_joint = -sum(sum(p_joint .* log2(p_joint + eps)));
    
    mi = h_true + h_pred - h_joint;
    
    % 计算 NMI
    nmi_value = mi / max(h_true, h_pred);
end
