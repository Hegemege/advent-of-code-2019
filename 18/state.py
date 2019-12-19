import math


class SearchState:
    def __init__(self):
        self.step_count = 0
        self.keys_picked = set()
        self.keys_missing = set()
        self.position = (0, 0)
        self.current_key = None

    def is_terminal_state(self):
        return len(self.keys_missing) == 0

    def clone(self):
        clone = SearchState()
        clone.step_count = self.step_count
        clone.keys_picked = self.keys_picked.copy()
        clone.keys_missing = self.keys_missing.copy()
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
        for k in self.keys_missing:
            target_position = key_position_lookup[k]

            cached_path_length = math.inf

            for paths in key_shortest_path_lookup[(self.current_key, k)]:
                path_length = paths[0]
                keys_used = paths[1]
                doors_fulfilled = 0
                for key in keys_used:
                    if key in self.keys_picked:
                        doors_fulfilled += 1
                if doors_fulfilled == len(keys_used):
                    # Use the cached path distance
                    cached_path_length = path_length

            if cached_path_length is not math.inf:
                actions.append((target_position, cached_path_length, k))
                continue

            # Calculate the path
            path_length_to_key = self.get_path_length(grid, target_position)
            door_cache = grid[target_position[1]][target_position[0]].find_parent_doors(
                []
            )

            # Add to cache
            key_shortest_path_lookup[(self.current_key, k)].append(
                (path_length_to_key, door_cache,)
            )

            key_shortest_path_lookup[(k, self.current_key)].append(
                (path_length_to_key, door_cache,)
            )

            if path_length_to_key is not math.inf:
                actions.append((target_position, path_length_to_key, k))

        # Sort actions such that shortest is last
        # actions.sort(key=lambda x: x[2], reverse=True)
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
                node.parent = None

        grid[self.position[1]][self.position[0]].set_depth(0, self.keys_missing)
        return grid[target_position[1]][target_position[0]].depth

    def apply_action(self, action):
        """
            Moves the position to the given position in the action 3-tuple
            Increments step count
        """
        self.position = action[0]
        self.step_count += action[1]
        self.keys_picked.add(action[2])
        self.keys_missing.remove(action[2])
        self.current_key = action[2]
