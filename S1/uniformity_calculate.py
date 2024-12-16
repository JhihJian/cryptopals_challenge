from collections import Counter
import math


def uniformity_index(data):
    if not data:
        return 0.0  # 空列表的均匀性指数为0

    # 计算数据的最大值和最小值
    data_min, data_max = min(data), max(data)

    # 确定区间数量（可以根据数据大小调整，这里使用sqrt(n)作为经验法则）
    num_bins = int(math.sqrt(len(data))) if len(data) > 1 else 1
    bin_width = (data_max - data_min) / num_bins if num_bins > 0 else 0
    if bin_width==0:
        return 0
    # 计算每个区间中的数据点数量
    bin_counts = Counter()
    for value in data:
        bin_index = int((value - data_min) // bin_width)
        if bin_index < num_bins:
            bin_counts[bin_index] += 1

    # 计算均匀性指数
    total_points = len(data)
    max_possible_count = total_points // num_bins  # 每个区间理想情况下的最大点数（向下取整）
    extra_points = total_points % num_bins  # 剩余的点数，这些点数将分配给某些区间

    # 计算每个区间的“理想”点数（尽量均匀分配）
    ideal_counts = [max_possible_count] * num_bins
    for i in range(extra_points):
        ideal_counts[i] += 1

    # 计算均匀性指数（使用曼哈顿距离衡量差异）
    uniformity = 1 - sum(abs(bin_counts[i] - ideal_counts[i]) for i in range(num_bins)) / (total_points * num_bins)

    # 由于我们可能没有完全均匀分配额外的点数，因此最终的指数可能需要稍微调整
    # 但为了简化，这里直接返回计算得到的值
    return uniformity


# # 示例使用
# data = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
# print(uniformity_index(data))  # 输出一个介于0和1之间的数值，表示分布的均匀性