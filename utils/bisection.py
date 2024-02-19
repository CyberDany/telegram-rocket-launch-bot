from typing import List, Tuple

class Bisection:
    @staticmethod
    def calculate_mid_point(range: List) -> int:
        """
        Calculates the midpoint of the given range.
        """
        range_start = range[0]
        range_end = range[1]
        return (range_start + range_end) // 2

    @staticmethod
    def update_range(user_response: str, current_range: List[int]) -> Tuple[List[int], int]:
        """
        Updates the search range based on the user's response and calculates the new midpoint.
        """
        mid_point = Bisection.calculate_mid_point(current_range)

        if user_response == "Yes":
            current_range[1] = mid_point
        else:
            current_range[0] = mid_point + 1

        new_mid_point = Bisection.calculate_mid_point(current_range)
        return current_range, new_mid_point