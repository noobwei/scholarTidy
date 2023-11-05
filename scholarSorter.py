import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

search_term = input("keyword: ")
threshold = int(input("citations threshold: "))
# 读取文本文件中的信息并转化为数据结构
input_file = f'{search_term}_author'
with open(input_file, "r") as file:
    lines = file.readlines()

author_data = {}
current_author = None

for line in lines:
    line = line.strip()
    if line.startswith("Author: "):
        current_author = line[len("Author: "):]
        author_data[current_author] = {"Total Citations": 0, "Top 3 Cited Papers": set()}
    elif line.startswith("Total Citations: "):
        author_data[current_author]["Total Citations"] = int(line[len("Total Citations: "):])
    elif line.startswith("- "):
        # 检查标题格式，将标题和引用分开
        parts = line.split(", Citations: ")
        if len(parts) == 2:
            title, citations = parts[0][2:], int(parts[1])
            author_data[current_author]["Top 3 Cited Papers"].add(title)

authority_experts = {author: data for author, data in author_data.items() if data["Total Citations"] > threshold}

# 创建学者关系图，只包含 authority_experts 中的数据
G = nx.Graph()  # 由于是共同论文，将图类型改为无向图

for author in authority_experts:
    data = author_data[author]
    G.add_node(author, total_citations=data["Total Citations"],node_size=500)

# 分析专家之间的共同论文并添加连接
for author1 in authority_experts:
    for author2 in authority_experts:
        if author1 != author2:
            common_papers = author_data[author1]["Top 3 Cited Papers"].intersection(author_data[author2]["Top 3 Cited Papers"])
            if common_papers:
                G.add_edge(author1, author2,color='green')

# 使用不同的布局算法
pos = nx.spring_layout(G, k=0.7)  # 调整k值来分散节点位置

# 调整节点间距和节点尺寸
plt.figure(figsize=(12, 10))
nx.draw(G, pos, with_labels=True, node_size=1500, node_color="lightblue", font_size=8, font_color="black", edge_color='green')
plt.show()
