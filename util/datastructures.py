import heapq
from typing import List

from models.cell import Open


class PriorityQueue:
    def __init__(self) -> None:
        self.heap: List = []
        self.tiebreaker_count = 0

    def pop(self) -> Open:
        if len(self.heap) == 0:
            raise Exception('Priority Queue is empty')

        _, _, cell = heapq.heappop(self.heap)
        return cell

    def push(self, cell: Open, priority: float):
        self.tiebreaker_count += 1
        heapq.heappush(self.heap, (priority, self.tiebreaker_count, cell))
