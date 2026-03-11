#!/usr/bin/env python3
"""Priority Queue variants — min-heap, max-heap, indexed, d-ary.

All from scratch without heapq.

Usage:
    python priority_queue.py --test
"""

import sys


class MinHeap:
    """Binary min-heap."""

    def __init__(self):
        self._data = []

    def push(self, item):
        self._data.append(item)
        self._sift_up(len(self._data) - 1)

    def pop(self):
        if not self._data:
            raise IndexError("pop from empty heap")
        self._swap(0, len(self._data) - 1)
        item = self._data.pop()
        if self._data:
            self._sift_down(0)
        return item

    def peek(self):
        if not self._data:
            raise IndexError("peek at empty heap")
        return self._data[0]

    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self._data[i] < self._data[parent]:
                self._swap(i, parent)
                i = parent
            else:
                break

    def _sift_down(self, i):
        n = len(self._data)
        while True:
            smallest = i
            left = 2 * i + 1
            right = 2 * i + 2
            if left < n and self._data[left] < self._data[smallest]:
                smallest = left
            if right < n and self._data[right] < self._data[smallest]:
                smallest = right
            if smallest != i:
                self._swap(i, smallest)
                i = smallest
            else:
                break

    def _swap(self, i, j):
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def __len__(self):
        return len(self._data)

    def __bool__(self):
        return bool(self._data)


class MaxHeap:
    """Binary max-heap (wraps MinHeap with negation)."""

    def __init__(self):
        self._heap = MinHeap()

    def push(self, priority, item):
        self._heap.push((-priority, item))

    def pop(self):
        neg_p, item = self._heap.pop()
        return -neg_p, item

    def peek(self):
        neg_p, item = self._heap.peek()
        return -neg_p, item

    def __len__(self):
        return len(self._heap)


class IndexedPQ:
    """Indexed priority queue — supports decrease-key in O(log n)."""

    def __init__(self):
        self._data = []      # [(priority, key), ...]
        self._index = {}     # key -> position in _data

    def push(self, key, priority):
        if key in self._index:
            self.decrease_key(key, priority)
            return
        pos = len(self._data)
        self._data.append((priority, key))
        self._index[key] = pos
        self._sift_up(pos)

    def pop(self):
        if not self._data:
            raise IndexError("empty")
        self._swap(0, len(self._data) - 1)
        priority, key = self._data.pop()
        del self._index[key]
        if self._data:
            self._sift_down(0)
        return key, priority

    def decrease_key(self, key, new_priority):
        if key not in self._index:
            raise KeyError(key)
        pos = self._index[key]
        old_priority = self._data[pos][0]
        if new_priority < old_priority:
            self._data[pos] = (new_priority, key)
            self._sift_up(pos)

    def __contains__(self, key):
        return key in self._index

    def __len__(self):
        return len(self._data)

    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self._data[i][0] < self._data[parent][0]:
                self._swap(i, parent)
                i = parent
            else:
                break

    def _sift_down(self, i):
        n = len(self._data)
        while True:
            smallest = i
            l, r = 2*i+1, 2*i+2
            if l < n and self._data[l][0] < self._data[smallest][0]:
                smallest = l
            if r < n and self._data[r][0] < self._data[smallest][0]:
                smallest = r
            if smallest != i:
                self._swap(i, smallest)
                i = smallest
            else:
                break

    def _swap(self, i, j):
        self._data[i], self._data[j] = self._data[j], self._data[i]
        self._index[self._data[i][1]] = i
        self._index[self._data[j][1]] = j


class DAryHeap:
    """D-ary min-heap (generalized)."""

    def __init__(self, d: int = 4):
        self.d = d
        self._data = []

    def push(self, item):
        self._data.append(item)
        self._sift_up(len(self._data) - 1)

    def pop(self):
        self._data[0], self._data[-1] = self._data[-1], self._data[0]
        item = self._data.pop()
        if self._data:
            self._sift_down(0)
        return item

    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) // self.d
            if self._data[i] < self._data[parent]:
                self._data[i], self._data[parent] = self._data[parent], self._data[i]
                i = parent
            else:
                break

    def _sift_down(self, i):
        n = len(self._data)
        while True:
            smallest = i
            for k in range(1, self.d + 1):
                child = self.d * i + k
                if child < n and self._data[child] < self._data[smallest]:
                    smallest = child
            if smallest != i:
                self._data[i], self._data[smallest] = self._data[smallest], self._data[i]
                i = smallest
            else:
                break

    def __len__(self):
        return len(self._data)


def test():
    print("=== Priority Queue Tests ===\n")

    # MinHeap
    h = MinHeap()
    for v in [5, 3, 8, 1, 4]:
        h.push(v)
    result = []
    while h:
        result.append(h.pop())
    assert result == [1, 3, 4, 5, 8]
    print(f"✓ MinHeap: {result}")

    # MaxHeap
    mh = MaxHeap()
    for v in [5, 3, 8, 1, 4]:
        mh.push(v, f"item_{v}")
    _, item = mh.pop()
    assert item == "item_8"
    print(f"✓ MaxHeap: top = {item}")

    # IndexedPQ with decrease-key
    ipq = IndexedPQ()
    ipq.push("A", 10)
    ipq.push("B", 5)
    ipq.push("C", 8)
    ipq.decrease_key("A", 3)
    key, pri = ipq.pop()
    assert key == "A" and pri == 3
    print(f"✓ IndexedPQ: decrease-key A:10→3, popped {key}:{pri}")

    # D-ary heap
    dh = DAryHeap(d=4)
    import random
    nums = list(range(100))
    random.shuffle(nums)
    for n in nums:
        dh.push(n)
    sorted_result = []
    while dh:
        sorted_result.append(dh.pop())
    assert sorted_result == list(range(100))
    print("✓ 4-ary heap: sorted 100 items correctly")

    # Stress test
    h2 = MinHeap()
    for _ in range(10000):
        h2.push(random.randint(0, 100000))
    prev = -1
    while h2:
        v = h2.pop()
        assert v >= prev
        prev = v
    print("✓ Stress test: 10K items sorted correctly")

    print("\nAll tests passed! ✓")


if __name__ == "__main__":
    test() if not sys.argv[1:] or sys.argv[1] == "--test" else None
