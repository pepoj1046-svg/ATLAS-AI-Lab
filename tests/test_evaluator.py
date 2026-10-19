import unittest
from atlas.evaluator import arithmetic, check_answer
from atlas.experiment import run_benchmark


class ArithmeticTests(unittest.TestCase):
    def test_parentheses(self):
        self.assertEqual(arithmetic("7 * (3 + 5)"), 56)

    def test_unary(self):
        self.assertEqual(arithmetic("-3 + 8"), 5)

    def test_correct_answer(self):
        self.assertTrue(check_answer("2**6-1", 63))

    def test_incorrect_answer(self):
        self.assertFalse(check_answer("12*4-3", 46))

    def test_rejects_code(self):
        with self.assertRaises(ValueError):
            arithmetic("__import__('os').system('echo nope')")

    def test_rejects_huge_power(self):
        with self.assertRaises(ValueError):
            arithmetic("2 ** 1000")

    def test_rejects_division_by_zero(self):
        with self.assertRaises(ValueError):
            arithmetic("5/0")

    def test_benchmark(self):
        report = run_benchmark()
        self.assertEqual(report["total"], 4)
        self.assertEqual(report["correct"], 3)


if __name__ == "__main__":
    unittest.main()
