
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Generator


@dataclass
class Direction:
    dx: int
    dy: int


class Directions(Direction, Enum):
    NORTH = 0, 1
    EAST = 1, 0
    SOUTH = 0, -1
    WEST = -1, 0
    NORTH_EAST = 1, 1
    SOUTH_EAST = 1, -1
    SOUTH_WEST = -1, -1
    NORTH_WEST = -1, 1


@dataclass
class Position:
    x: int
    y: int

    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def generate_neighbors(self) -> Generator['Position', None, None]:
        return (Position(self.x + direction.dx, self.y + direction.dy) 
                for direction in Directions 
                if 0 <= self.x + direction.dx < 140 and 0 <= self.y + direction.dy < 140)


@dataclass
class Landmark:
    id: int
    position: Position


@dataclass
class Digit(Landmark):
    value: int


input_path = "C:\\repo_depot\\advent_of_code_2023\\day4\\input.txt"


def first_pass_process( __input_path: str, do_gear_stuff: bool = False) -> tuple[list[list[Digit]], list[list[Landmark]]]:
    with open(__input_path, "r") as f:
        all_landmarks: list[list[Landmark]] = []
        all_digits: list[list[Digit]]= []
        landmark_id = -1
        digit_id = -1

        for i, line in enumerate(f):
            landmarks: list[Landmark] = []
            digits: list[Digit] = []
            for j, c in enumerate(line.strip()):
                if c == ".":
                    continue
                if c.isdigit():
                    previous_digit: Digit = digits[-1] if digits else None

                    if not (previous_digit and previous_digit.position.x == j - 1):
                        digit_id += 1
                    
                    digits.append(Digit(digit_id, Position(j, i), int(c)))

                elif not do_gear_stuff:
                    landmark_id += 1
                    landmarks.append(Landmark(landmark_id, Position(j, i)))
                
                elif c == "*":
                    landmark_id += 1
                    landmarks.append(Landmark(landmark_id, Position(j, i)))
            all_digits.append(digits)
            all_landmarks.append(landmarks)
    
    return all_digits, all_landmarks


def second_pass_process( __all_digits: list[list[Digit]]
                       , __all_landmarks: list[list[Landmark]]
                       ) -> tuple[ dict[Position, int]
                                 , dict[Position, int]
                                 , defaultdict[int, list[int]]
                                 , defaultdict[int, list[int]]]:

    position_to_id__digits: dict[Position, int] = {}
    position_to_id__landmarks: dict[Position, int] = {}
    id_to_values__digits: dict[int, list[int]] = defaultdict(list[int])
    id_to_values__landmarks: dict[int, list[int]] = defaultdict(list[int])

    for digits_row, landmarks_row in zip(__all_digits, __all_landmarks):
        for digit in digits_row:
            position_to_id__digits[digit.position] = digit.id
            id_to_values__digits[digit.id].append(digit.value)
        for landmark in landmarks_row:
            position_to_id__landmarks[landmark.position] = landmark.id
            id_to_values__landmarks[landmark.id].append(landmark.id)

    return position_to_id__digits, position_to_id__landmarks, id_to_values__digits, id_to_values__landmarks


def third_pass_process( __position_to_id__digits: dict[Position, int]
                      , all_landmarks: list[list[Landmark]]
                      ) -> defaultdict[int, list[int]]:
    id_to_neighbors: defaultdict[int, list[int]] = defaultdict(list[int])
    for landmarks_row in all_landmarks:
        for landmark in landmarks_row:
            for neighbor_position in landmark.position.generate_neighbors():
                if neighbor_position in __position_to_id__digits:
                    id_to_neighbors[landmark.id].append(__position_to_id__digits[neighbor_position])
    return id_to_neighbors

def fourth_pass_process( __id_to_neighbors: defaultdict[int, list[int]] ) -> set[int]:
    all_neighbors = set()
    for neighbors in __id_to_neighbors.values():
        all_neighbors.update(neighbors)
    return all_neighbors

def final_pass_process( __all_neighbors: set[int]
                      , __id_to_values__digits: dict[int, list[int]] ) -> list[int]:
    all_values = []
    for id in __all_neighbors:
        value = 0
        for i, v in enumerate(__id_to_values__digits[id]):
            value += v * 10 ** (len(__id_to_values__digits[id]) - i - 1)
        all_values.append(value)
    return all_values


def do_gear_stuff( __id_to_neighbors: defaultdict[int, list[int]]
                 , __id_to_values__digits: dict[int, list[int]]):
    gear_pairs: list[list[int, int]] = []
    for _, neighbors in __id_to_neighbors.items():
        if len(set(neighbors)) == 2:
            gear_pairs.append(list(set(neighbors)))
    for gear_pair in gear_pairs:
        for i, id in enumerate(gear_pair):
            value = 0
            for j, v in enumerate(__id_to_values__digits[id]):
                value += v * 10 ** (len(__id_to_values__digits[id]) - j - 1)
            gear_pair[i] = value
    return gear_pairs
            

def main():
    all_digits, all_landmarks = first_pass_process(input_path, True)
    position_to_id__digits, _, id_to_values__digits, _ = second_pass_process(all_digits, all_landmarks)
    id_to_neighbors = third_pass_process(position_to_id__digits, all_landmarks)
    all_neighbors = fourth_pass_process(id_to_neighbors)    
    all_values = final_pass_process(all_neighbors, id_to_values__digits)
    print(sum(all_values))

    gear_pairs = do_gear_stuff(id_to_neighbors, id_to_values__digits)
    gear_mults = [gear_pair[0] * gear_pair[1] for gear_pair in gear_pairs]
    print(sum(gear_mults))

if __name__ == "__main__":
    main()