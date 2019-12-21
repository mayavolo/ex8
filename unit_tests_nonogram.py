import unittest
import nonogram


class MyTestCase(unittest.TestCase):
    def test_get_row_variations(self):
        self.assertEqual([[1, 1, 0, 1, 1, 1, 0, 1]],
                         nonogram.get_row_variations([-1, -1, -1, -1, -1, -1, -1, -1], [2, 3, 1]))

    def test_add_allowed_rows(self):
        self.assertEqual([[1, 2, 3], [3, 4, 5]], nonogram.add_allowed_row([[1, 2, 3]], [[3, 4, 5]], 12))

    def test_get_intersection_row(self):
        self.assertEqual([-1, 1, 1, -1], nonogram.get_intersection_row([[0, 1, 1, 1], [1, 1, 1, 0]]))

    def test_solve_easy_nonogram(self):
        self.assertEqual([[1, 1], [0, 0]], nonogram.solve_easy_nonogram([[[2], []], [[1], [1]]]))


if __name__ == '__main__':
    unittest.main()
