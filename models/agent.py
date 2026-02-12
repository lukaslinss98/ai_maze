from models.cell import Open


class Agent:
    def __init__(self, starting_cell: Open) -> None:
        self.current_cell = starting_cell
