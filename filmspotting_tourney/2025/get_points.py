from collections import defaultdict
from pathlib import Path


def calculate_movie_points(file_path: Path) -> dict:
    # Initialize dictionary with default value 0
    movie_points = defaultdict(int)

    # Read file and process lines
    with open(file_path) as f:
        lines = [line.strip().rstrip(',') for line in f if line.strip()]

    # Process each group of 4 lines
    for i, movie in enumerate(lines):
        # Calculate points based on position within group of 4
        position = (i % 4)
        points = 4 - position  # 4,3,2,1 points for positions 0,1,2,3
        movie_points[movie] += points

    return dict(sorted(movie_points.items(), key=lambda x: x[1], reverse=True))


def print_results(points_dict: dict):
    print("\nMovie Points:")
    print("-" * 50)
    for movie, points in points_dict.items():
        print(f"{movie}: {points}")


if __name__ == "__main__":
    file_path = Path('../../results/2025_final_four.txt')
    points = calculate_movie_points(file_path)
    print_results(points)