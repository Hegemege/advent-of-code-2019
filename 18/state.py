import math


class SearchState:
    def __init__(self):
        self.step_count = 0
        self.keys_picked = {}
        self.position = (0, 0)
        self.current_key = None

    def is_terminal_state(self):
        return sum([v for k, v in self.keys_picked.items()]) == len(self.keys_picked)

    def clone(self):
        clone = SearchState()
        clone.step_count = self.step_count
        clone.keys_picked = self.keys_picked.copy()
        clone.position = (self.position[0], self.position[1])
        clone.current_key = self.current_key
        return clone

    def get_actions(self, grid, key_position_lookup, key_shortest_path_lookup):
        """
            Returns a 3-tuple ((x, y), steps, key_symbol)
            x: Target x position
            y: Target y position
            steps: Steps required to reach (x, y)
            key_symbol: Symbol of the picked key
        """
        actions = []

        # For every key not yet picked, see if we can reach them
        for k, v in self.keys_picked.items():
            if v is True:
                continue

            target_position = key_position_lookup[k]

            cached_path_length = math.inf
            # Check if the path has been cached and we have all the keys required
            if self.step_count > 0:  # First step does not start from a key
                path_length = math.inf
                doors = []
                if (self.current_key, k) in key_shortest_path_lookup:
                    path_length, doors = key_shortest_path_lookup[(self.current_key, k)]
                elif (k, self.current_key) in key_shortest_path_lookup:
                    path_length, doors = key_shortest_path_lookup[(k, self.current_key)]

                if path_length is not math.inf:
                    doors_fulfilled = 0
                    for door in doors:
                        if self.keys_picked[door.lower()]:
                            doors_fulfilled += 1
                    if doors_fulfilled == len(doors):
                        # Use the cached path distance
                        cached_path_length = path_length

            if cached_path_length is not math.inf:
                actions.append((target_position, cached_path_length, k))
                continue

            path_length_to_key = self.get_path_length(grid, target_position)

            if path_length_to_key is not math.inf:
                actions.append((target_position, path_length_to_key, k))

        return actions

    def get_path_length(self, grid, target_position):
        """
            Returns the shortest distance to the target position
            for the current state
        """
        # First clear current depths
        for row in grid:
            for node in row:
                node.depth = math.inf

        grid[self.position[1]][self.position[0]].set_depth(0, self.keys_picked)
        return grid[target_position[1]][target_position[0]].depth

    def apply_action(self, action):
        """
            Moves the position to the given position in the action 3-tuple
            Increments step count
        """
        self.position = action[0]
        self.step_count += action[1]
        self.keys_picked[action[2]] = True
        self.current_key = action[2]
