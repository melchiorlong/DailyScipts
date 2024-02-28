import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.font_manager import FontProperties

fig, ax = plt.subplots(figsize=(10, 12))

cn_font = FontProperties(fname='/Users/tianlong/PycharmProjects/DailyScipts/ZX_Work/BurialPoint/STHeiti Light.ttc',
                         size=14)

# List of steps
steps = [
    "确定埋点目标",
    "设计埋点策略",
    "埋点代码实现",
    "测试环境验证",
    "数据一致性检查",
    "性能测试",
    "实时监控",
    "异常报警",
    "数据分析与反馈",
    "优化迭代",
    "文档记录",
    "团队培训"
]

# Drawing parameters
box_height = 0.8
box_width = 4
spacing_y = 1.5
initial_y = 0
arrow_params = dict(facecolor="black", arrowstyle="-|>", lw=1)
text_params = dict(ha="center", va="center", fontproperties=cn_font, fontsize=12, weight="bold")

# Drawing boxes and arrows
for i, step in enumerate(steps):
    rect = mpatches.FancyBboxPatch((initial_y, -i * spacing_y), box_width, -box_height,
                                   boxstyle="round,pad=0.1", ec="black", fc="lightblue")
    ax.add_patch(rect)
    ax.text(initial_y + box_width / 2, -i * spacing_y - box_height / 2, step, **text_params)
    if i < len(steps) - 1:
        ax.annotate("", xy=(initial_y + box_width / 2, -i * spacing_y - box_height),
                    xytext=(initial_y + box_width / 2, -(i + 1) * spacing_y + box_height),
                    arrowprops=arrow_params)

# Adjusting the plot
ax.set_xlim(-1, 5)
ax.set_ylim(-len(steps) * spacing_y, 1)
ax.axis("off")

plt.title("埋点测试流程图", fontsize=14, weight="bold", fontproperties=cn_font)
plt.show()
