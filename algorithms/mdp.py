from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass
from time import perf_counter
from typing import List, Union

from models.cell import Open
from models.maze import MdpMaze


@dataclass(frozen=True)
class Snapshot:
    maze: MdpMaze
    delta_v: float


@dataclass(frozen=True)
class PolicySnapshot:
    maze: MdpMaze
    delta_v: float
    mode: str
    eval_iters: int
    improve_iters: int


@dataclass(frozen=True)
class MdpResult:
    snapshots: List[Snapshot]
    shortest_path: List[Open]
    run_time: float


@dataclass(frozen=True)
class PolicyResult:
    snapshots: List[PolicySnapshot]
    shortest_path: List[Open]
    run_time: float
    total_eval_iterations: int
    total_improve_iterations: int


class MdpAlgorithm(ABC):
    @abstractmethod
    def solve(self, maze: MdpMaze) -> Union[MdpResult, PolicyResult]:
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


class PolicyIteration(MdpAlgorithm):
    def __init__(
        self, discount: float, living_reward: float, noise=0.2, theta=0.0001
    ) -> None:
        self.discount = discount
        self.living_reward = living_reward
        self.noise = noise
        self.theta = theta

    def solve(self, maze: MdpMaze) -> PolicyResult:
        snapshots = []
        eval_iters = 0
        improve_iters = 0
        start_time = perf_counter()
        delta = float('inf')
        is_stable = False

        while not is_stable:
            while delta > self.theta:
                delta = self._policy_evaluation_step(maze)
                eval_iters += 1
                snapshot = PolicySnapshot(
                    deepcopy(maze), delta, 'eval', eval_iters, improve_iters
                )
                snapshots.append(snapshot)

            is_stable = self._policy_improvement_step(maze)
            improve_iters += 1
            snapshot = PolicySnapshot(
                deepcopy(maze), 0.0, 'improve', eval_iters, improve_iters
            )
            snapshots.append(snapshot)
            delta = float('inf')

        run_time = perf_counter() - start_time
        shortest_path = maze.shortest_path(maze.start, maze.end)
        return PolicyResult(
            snapshots, shortest_path, run_time, eval_iters, improve_iters
        )

    def _policy_evaluation_step(self, maze: MdpMaze) -> float:
        max_delta_v = float('-inf')
        for cell in maze.get_open_cells():
            if cell == maze.end:
                continue

            old_value = cell.value
            exp_value = maze.value_by_action(cell, self.noise)[cell.policy]
            cell.value = self.living_reward + self.discount * exp_value
            dV = abs(cell.value - old_value)
            max_delta_v = max(max_delta_v, dV)

        return max_delta_v

    def _policy_improvement_step(self, maze: MdpMaze) -> bool:
        is_stable = True

        for cell in maze.get_open_cells():
            if cell == maze.end:
                continue

            old_policy = cell.policy
            max_value = float('-inf')
            for action, neighbor in maze.neighbors(cell):
                if neighbor.value > max_value:
                    max_value = neighbor.value
                    cell.policy = action

            if old_policy != cell.policy:
                is_stable = False

        return is_stable
