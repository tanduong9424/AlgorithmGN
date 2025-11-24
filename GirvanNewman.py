import networkx as nx
from networkx.algorithms.community import girvan_newman
from networkx.algorithms.community.quality import modularity
import time

# 1) đọc file input chuyển thành đồ thị
G = nx.Graph()
with open("./karate.mtx", "r") as f: # đọc karate club 
#with open("./dolphins.mtx", "r") as f: # đọc dolphins network
    for line in f:
        if line.startswith("%"): # bỏ qua mấy dòng có % chứa thông tin thêm về dataset
            continue
        parts = line.strip().split() # bỏ qua luôn cái dòng chứ số đỉnh, số cạnh luôn bởi thư viện tự tính được
        if len(parts) == 3:
            continue
        if len(parts) == 2: # lọc ra lấy 2 đỉnh nối với nhau
            u, v = map(int, parts)
            G.add_edge(u, v)

print("Số đỉnh:", G.number_of_nodes())
print("Số cạnh:", G.number_of_edges())

# 2) chạy Girvan-Newman và tính modularity
comp_gen = girvan_newman(G)

best_mod = -1
best_partition = None
step = 0
start_total = time.perf_counter() # bắt đầu tính thời gian chạy Girvan-Newman
for communities in comp_gen:
    step += 1
    partition = [list(c) for c in communities]
    m = modularity(G, communities) # tính modularity

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
print(len(best_partition)," phân vùng tốt nhất:", best_partition)
print("Modularity đạt cực đại với giá trị:", best_mod)
print(f"Tổng thời gian chạy thuật toán: {total_time:.6f} giây")
