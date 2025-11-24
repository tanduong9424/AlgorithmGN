import networkx as nx
from networkx.algorithms.community import girvan_newman
from networkx.algorithms.community.quality import modularity
import time
import matplotlib.pyplot as plt

# 1) đọc file input chuyển thành đồ thị
G = nx.Graph()
with open("./ego-facebook.edges", "r") as f: # đọc karate club 
#with open("./ego-twitter.edges", "r") as f: # đọc karate club 
#with open("./karate.mtx", "r") as f: # đọc karate club 
#with open("./dolphins.mtx", "r") as f: # đọc dolphins network
    for line in f:
        line = line.strip()
        if not line:
            continue
        if line.startswith("%"):
            continue
        line_clean = line.replace(',', ' ') # nếu trường hợp các đỉnh ngăn cách bởi dấu phẩy
        parts = line_clean.split()
        if len(parts) < 2:
            continue
        try:
            u = int(parts[0])
            v = int(parts[1])
        except ValueError:
            continue
        G.add_edge(u, v)

print("Số đỉnh:", G.number_of_nodes())
print("Số cạnh:", G.number_of_edges())


# 2) chạy Girvan-Newman và tính modularity
comp_gen = girvan_newman(G)

best_mod = -1
best_partition = None
step = 0
mods = [] #mảng lưu modularity để vẽ biểu đồ modularity theo từng bước
start_total = time.perf_counter() # bắt đầu tính thời gian chạy Girvan-Newman
for communities in comp_gen:
    step += 1
    partition = [list(c) for c in communities]
    m = modularity(G, communities) # tính modularity
    mods.append(m) # thêm giá trị m vào mảng mods

    print(f"\nBước{step}---------------------------------")
    print("Partition:", partition)
    print("Số cộng đồng :", len(partition))
    print("Modularity:", m)

    if m > best_mod:
        best_mod = m
        best_partition = partition
    else:
        break

end_total = time.perf_counter()   # kết thúc tính thời gian chạy GN
total_time = end_total - start_total

# 3) Kết quả cuối cùng

print("\n-----------------------------")
print("KẾT QUẢ CUỐI CÙNG:")
print("Phát hiện được ", len(best_partition), "cộng đồng.")
#print(len(best_partition)," phân vùng tốt nhất:", best_partition)
print("Modularity đạt cực đại với giá trị:", best_mod)
print(f"Tổng thời gian chạy thuật toán: {total_time:.6f} giây")


'''
# VẼ ĐỒ THỊ MODULARITY
plt.figure(figsize=(6, 4))
plt.plot(range(1, len(mods) + 1), mods, marker='o')
plt.xlabel('Bước')
plt.ylabel('Modularity')
plt.title('Modularity theo từng bước Girvan-Newman')
plt.grid(True)
plt.tight_layout()
plt.show()

# VẼ LẠI CỘNG ĐỒNG KHI MODULARITY ĐẠT CỰC ĐẠI
pos = nx.spring_layout(G, seed=42)
cmap = plt.get_cmap('tab20')
node_color_map = {}
for i, community in enumerate(best_partition):
    for node in community:
        node_color_map[node] = cmap(i % 20)
node_colors = [node_color_map.get(node, (0.6, 0.6, 0.6)) for node in G.nodes()]
plt.figure(figsize=(8, 6))
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=150)
nx.draw_networkx_edges(G, pos, alpha=0.5)
nx.draw_networkx_labels(G, pos, font_size=8)
modularity_print = int(best_mod * 1000) / 1000 # lấy 3 số sau dấu phẩy, ko làm tròn
plt.title(f"Modularity≈{modularity_print}")
plt.axis('off')
plt.tight_layout()
plt.show()

'''