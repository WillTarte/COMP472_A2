import unittest
from xpuzzle import XPuzzle
from typing import List, Tuple, Dict
import numpy as np
import traceback


class TestXPuzzle(unittest.TestCase):
    def test_from_array_should_pass(self):
        data_array: List[int] = [3, 0, 1, 4, 2, 6, 5, 7]
        to_test: XPuzzle = XPuzzle.from_array(data_array)
        self.assertTrue(
            np.array_equal(np.array([[3, 0, 1, 4], [2, 6, 5, 7]]), to_test.state),
            "Should be equivalent",
        )
        self.assertEqual((2, 4), to_test.shape, "Should be equivalent")

    def test_from_array_wrong_size_should_fail(self):
        data_array1: List[int] = [3, 0, 1, 4, 2, 6, 5, 7]
        with self.assertRaises(AssertionError):
            XPuzzle.from_array(data_array1, (1, 1))

        data_array2: List[int] = [3, 0, 1, 4, 2, 6, 5, 7, 8]
        with self.assertRaises(AssertionError):
            XPuzzle.from_array(data_array2)

        data_array3: List[int] = [3, 0, 1, 4, 2, 6]
        with self.assertRaises(AssertionError):
            XPuzzle.from_array(data_array3)

    def test_repr_should_pass(self):
        data_array: List[int] = [3, 0, 1, 4, 2, 6, 5, 7]
        to_test: XPuzzle = XPuzzle.from_array(data_array)
        expected = "3 0 1 4\n2 6 5 7"
        result = to_test.__repr__()
        self.assertEqual(expected, result, "Should be the same")

    def test_from_array_custom_size_should_pass(self):
        data_array: List[int] = [
            3,
            0,
            1,
            4,
            2,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
        ]
        puzzle_to_test1 = XPuzzle.from_array(data_array, (3, 6))
        puzzle_to_test2 = XPuzzle.from_array(data_array, (6, 3))

        self.assertTrue(
            np.array_equal(
                np.array(
                    [[3, 0, 1, 4, 2, 5], [6, 7, 8, 9, 10, 11], [12, 13, 14, 15, 16, 17]]
                ),
                puzzle_to_test1.state,
            ),
            "Should be True",
        )
        self.assertEqual((3, 6), puzzle_to_test1.shape, "Should be equivalent")

        self.assertTrue(
            np.array_equal(
                np.array(
                    [
                        [3, 0, 1],
                        [4, 2, 5],
                        [6, 7, 8],
                        [9, 10, 11],
                        [12, 13, 14],
                        [15, 16, 17],
                    ]
                ),
                puzzle_to_test2.state,
            ),
            "Should be True",
        )
        self.assertEqual((6, 3), puzzle_to_test2.shape, "Should be equivalent")

    def test_from_file_should_pass(self):
        puzzles_to_test: List[XPuzzle] = XPuzzle.from_file(r"./samplePuzzles.txt")

        self.assertEqual(3, len(puzzles_to_test), "There should be 3 puzzles")

        self.assertTrue(
            np.array_equal(
                np.array([[3, 0, 1, 4], [2, 6, 5, 7]]), puzzles_to_test[0].state
            ),
            "Should be True",
        )
        self.assertEqual((2, 4), puzzles_to_test[0].shape, "should be equivalent")

        self.assertTrue(
            np.array_equal(
                np.array([[6, 3, 4, 7], [1, 2, 5, 0]]), puzzles_to_test[1].state
            ),
            "Should be True",
        )
        self.assertEqual((2, 4), puzzles_to_test[1].shape, "should be equivalent")

        self.assertTrue(
            np.array_equal(
                np.array([[1, 0, 3, 6], [5, 2, 7, 4]]), puzzles_to_test[2].state
            ),
            "Should be equivalent",
        )
        self.assertEqual((2, 4), puzzles_to_test[2].shape, "should be equivalent")

    def test_eq_should_pass(self):
        puzzle1 = XPuzzle.from_array([3, 0, 1, 4, 2, 6, 5, 7])
        puzzle2 = XPuzzle.from_array([3, 0, 1, 4, 2, 6, 5, 7])
        self.assertTrue(puzzle1 == puzzle2)

    def test_is_goal_state_should_pass(self):
        puzzle1 = XPuzzle.from_array([1, 2, 3, 4, 5, 6, 7, 0])
        puzzle2 = XPuzzle.from_array([1, 3, 5, 7, 2, 4, 6, 0])
        self.assertTrue(puzzle1.is_goal_state())
        self.assertTrue(puzzle2.is_goal_state())

    def test_is_goal_state_false_should_pass(self):
        puzzle1 = XPuzzle.from_array([1, 2, 3, 5, 0, 4, 6, 7])
        puzzle2 = XPuzzle.from_array([1, 2, 3, 4, 5, 6, 0, 7])
        puzzle3 = XPuzzle.from_array([1, 3, 5, 7, 2, 4, 0, 6])
        puzzle4 = XPuzzle.from_array([2, 4, 6, 7, 1, 3, 5, 0])
        puzzle5 = XPuzzle.from_array([5, 6, 7, 0, 1, 2, 3, 4])

        self.assertFalse(puzzle1.is_goal_state())
        self.assertFalse(puzzle2.is_goal_state())
        self.assertFalse(puzzle3.is_goal_state())
        self.assertFalse(puzzle4.is_goal_state())
        self.assertFalse(puzzle5.is_goal_state())

    def test_find_valid_moves_should_pass(self):
        try:
            puzzle = XPuzzle.from_array([3, 0, 1, 4, 2, 6, 5, 7])
            puzzle.find_valid_moves()
        except Exception as exc:
            self.fail(traceback.format_exc())

if __name__ == "__main__":
    unittest.main()

    #data_array: List[int] = [3, 0, 1, 4, 2, 6, 5, 7]
    #to_test: XPuzzle = XPuzzle.from_array(data_array)
    #print(to_test)

    #to_test.find_valid_moves()
    #for x in to_test.valid_moves:
    #    print(x)

    #puzzle = XPuzzle.from_array([1, 2, 3, 5, 0, 4, 6, 7])
    #print(puzzle.is_goal_state())