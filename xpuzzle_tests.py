import unittest
from xpuzzle import XPuzzle
from typing import List, Tuple, Dict

class TestXPuzzle(unittest.TestCase):

    def test_from_array_should_pass(self):
        data_array: List[int] = [3, 0, 1, 4, 2, 6, 5, 7]
        to_test: XPuzzle = XPuzzle.from_array(data_array)
        self.assertEqual(data_array, to_test.state, "Should be equivalent")
        self.assertEqual((2,4), to_test.size, "Should be equivalent")

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
        data_array: List[int] = [3, 0, 1, 4, 2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
        puzzle_to_test1 = XPuzzle.from_array(data_array, (3,6))
        puzzle_to_test2 = XPuzzle.from_array(data_array, (6,3))

        self.assertEqual(data_array, puzzle_to_test1.state, "Should be equivalent")
        self.assertEqual((3,6), puzzle_to_test1.size, "Should be equivalent")

        self.assertEqual(data_array, puzzle_to_test2.state, "Should be equivalent")
        self.assertEqual((6,3), puzzle_to_test2.size, "Should be equivalent")

    def test_from_file_should_pass(self):
        puzzles_to_test: List[XPuzzle] = XPuzzle.from_file(r"./samplePuzzles.txt")

        self.assertEqual(3, len(puzzles_to_test), "There should be 3 puzzles")

        self.assertEqual([3, 0, 1, 4, 2, 6, 5, 7], puzzles_to_test[0].state, "Should be equivalent")
        self.assertEqual((2,4), puzzles_to_test[0].size, "should be equivalent")
        
        self.assertEqual([6, 3, 4, 7, 1, 2, 5, 0], puzzles_to_test[1].state, "Should be equivalent")
        self.assertEqual((2,4), puzzles_to_test[1].size, "should be equivalent")

        self.assertEqual([1, 0, 3, 6, 5, 2, 7, 4], puzzles_to_test[2].state, "Should be equivalent")
        self.assertEqual((2,4), puzzles_to_test[2].size, "should be equivalent")




if __name__ == "__main__":
    unittest.main()