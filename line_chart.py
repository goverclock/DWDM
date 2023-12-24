import matplotlib.pyplot as plt

# /System/Library/AssetsV2/com_apple_MobileAsset_Font7/8dc7805506cc9f233dcc19aabf593196842a47ae.asset/AssetData/Hannotate.ttc
plt.rcParams['font.sans-serif']=['SimHei','Songti SC','STFangsong']
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


# 参数说明（不能使用中文）：x轴数据一维数组,y轴数据二维数组,标题，x轴说明，y轴说明，每组x轴数据所对应的折线名称（每一项可以为空但是不能不对应）
def plot_line_chart(
    x_values,
    y_values_list,
    title="line chart",
    x_label="X",
    y_label="Y",
    legend_labels=None,
):
    plt.figure()

    for i, y_values in enumerate(y_values_list):
        label = legend_labels[i]
        plt.plot(x_values, y_values, label=label)

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.grid(True)

    y_min = min(min(y_values) for y_values in y_values_list)
    y_max = max(max(y_values) for y_values in y_values_list)
    # x_min, x_max = min(x_values), max(x_values)

    # 设置图表的大小，可以根据需要调整比例
    # plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)

    plt.show()


# 示例：
# x_values = [1, 4, 9, 16, 25]
# y_values_list = [[1, 2, 3, 4, 5], [1, 2, 4, 8, 16]]  # 两个数据集的x坐标
# legend_labels = ["1", "2"]

# plot_line_chart(x_values, y_values_list, legend_labels=legend_labels)
