from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass
from time import perf_counter
from typing import List

from models.cell import Open
from models.maze import MdpMaze


@dataclass(frozen=True)
class Snapshot:
    maze: MdpMaze
    delta_v: float


@dataclass(frozen=True)
class MdpResult:
    snapshots: List[Snapshot]
    shortest_path: List[Open]
    run_time: float


class MdpAlgorithm(ABC):
    @abstractmethod
    def solve(self, maze: MdpMaze) -> MdpResult:
        pass


class ValueIteration(MdpAlgorithm):
    def __init__(
        self, discount: float, living_reward: float, noise=0.2, theta=0.0001
    ) -> None:
        self.discount = discount
        self.living_reward = living_reward
        self.noise = noise
        self.theta = theta

    def solve(self, maze: MdpMaze) -> MdpResult:
        delta_V = float('inf')
        snapshots = []
        start_time = perf_counter()
        while delta_V > self.theta:
            delta_V = self._value_iteration_step(maze)

            snapshot = Snapshot(deepcopy(maze), delta_V)
            snapshots.append(snapshot)

        run_time = perf_counter() - start_time
        shortest_path = maze.shortest_path(maze.start, maze.end)
        return MdpResult(snapshots, shortest_path, run_time)

    def _value_iteration_step(self, maze: MdpMaze) -> float:
        max_diff_value = 0.0
        for cell in maze.get_open_cells():
            if cell == maze.end:
                continue

            value_by_action = maze.value_by_action(cell, self.noise)

            if value_by_action:
                best_direction = max(value_by_action, key=lambda a: value_by_action[a])
                max_q = value_by_action[best_direction]

                old_value = cell.value
                new_value = self.living_reward + self.discount * max_q

                max_diff_value = max(max_diff_value, abs(new_value - old_value))
                cell.value = new_value
                cell.policy = best_direction

        return max_diff_value
