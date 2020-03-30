class IndexedMinHeap:

    def __init__(self, key=lambda x: x, custom_hash=lambda x: x):
        self.key = key
        self.custom_hash = custom_hash
        self._heap = []
        self._item_to_index = {}

    def insert(self, item):
        self._heap.append(item)
        self._item_to_index[self.custom_hash(item)] = len(self._heap) - 1
        self._siftdown(len(self._heap) - 1)

    def contains(self, item):
        if self.custom_hash(item) in self._item_to_index:
            return True

    def value_of(self, item):
        return self.key(self._heap[self._item_to_index[self.custom_hash(item)]])

    def _siftdown(self, position):
        current = position
        item = self._heap[current]
        while current > 0:
            parent = (current - 1) // 2
            if self.key(item) < self.key(self._heap[parent]):
                self._heap[current] = self._heap[parent]
                self._item_to_index[self.custom_hash(self._heap[parent])] = current
                current = parent
            else:
                break
        self._heap[current] = item
        self._item_to_index[self.custom_hash(item)] = current

    def delete(self, item):
        index = self._item_to_index[self.custom_hash(item)]
        del self._item_to_index[self.custom_hash(item)]
        if index == len(self._heap) - 1:
            self._heap.pop()
            return
        self._heap[index] = self._heap.pop()
        self._item_to_index[self.custom_hash(self._heap[index])] = index
        self._siftup(index)
        self._siftdown(index)

    def _siftup(self, index):
        item = self._heap[index]
        current = index
        while 2 * current + 1 < len(self._heap):
            lesser_child = 2 * current + 1
            righ_child = 2 * current + 2
            if righ_child < len(self._heap) and self.key(self._heap[righ_child]) < self.key(self._heap[lesser_child]):
                lesser_child = righ_child
            if self.key(item) > self.key(self._heap[lesser_child]):
                self._heap[current] = self._heap[lesser_child]
                self._item_to_index[self.custom_hash(self._heap[lesser_child])] = current
                current = lesser_child
            else:
                break
        self._heap[current] = item
        self._item_to_index[self.custom_hash(item)] = current

    def pop(self):
        del self._item_to_index[self.custom_hash(self._heap[0])]
        if len(self._heap) > 1:
            item = self._heap[0]
            self._heap[0] = self._heap.pop()
            self._item_to_index[self.custom_hash(self._heap[0])] = 0
            self._siftup(0)
        else:
            item = self._heap.pop()
        return item
        
class PrimMST:
    def __init__(self, graph_file):
        self._graph = {}
        self._cost = 0
        with open(graph_file, "r") as file:
            num_vertices, num_edges = (int(num) for num in file.readline().split())
            for i in range(1, num_vertices + 1):
                self._graph[i] = []
            for i in range(num_edges):
                from_vertex, to_vertex, weight = (int(num) for num in file.readline().split())
                self._graph[from_vertex].append((to_vertex, weight))
                self._graph[to_vertex].append((from_vertex, weight))
        self._compute_mst()

    def get_cost(self):
        return self._cost

    def _compute_mst(self):
        unvisited = set(self._graph.keys())
        heap = IndexedMinHeap(key=lambda x: x[1], custom_hash=lambda x: x[0])
        visited = set()
        visited.add(1)
        heap.insert((1, 0))
        while unvisited:
            new_vertex = heap.pop()
            self._cost += new_vertex[1]
            unvisited.remove(new_vertex[0])
            visited.add(new_vertex[0])
            for edge in self._graph[new_vertex[0]]:
                if edge[0] not in visited:
                    if heap.contains(edge):
                        if heap.value_of(edge) >= edge[1]:
                            heap.delete(edge)
                            heap.insert(edge)
                    else:
                        heap.insert(edge)

if __name__ == "__main__":
    prim = PrimMST("edges.txt")
    print(prim.get_cost())
