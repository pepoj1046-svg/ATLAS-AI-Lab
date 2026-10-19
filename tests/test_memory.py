import os
import tempfile
import unittest
from atlas.memory import VerifiedMemory
from atlas.comparison import compare


class MemoryTests(unittest.TestCase):
    def test_persistence(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "memory.sqlite3")
            memory = VerifiedMemory(path)
            memory.add_verified("L1", "addition", "compute_sum")
            memory.close()
            reopened = VerifiedMemory(path)
            self.assertEqual(reopened.retrieve("addition"), "compute_sum")
            reopened.close()

    def test_no_unknown_rule(self):
        memory = VerifiedMemory()
        with self.assertRaises(ValueError):
            memory.add_verified("L2", "addition", "delete_everything")
        memory.close()

    def test_no_mismatched_rule(self):
        memory = VerifiedMemory()
        with self.assertRaises(ValueError):
            memory.add_verified("L3", "addition", "compute_product")
        memory.close()

    def test_comparison(self):
        result = compare()
        self.assertEqual(result["total"], 6)
        self.assertEqual(result["baseline_correct"], 0)
        self.assertEqual(result["memory_correct"], 6)
        self.assertTrue(set(result["train_ids"]).isdisjoint(result["holdout_ids"]))


if __name__ == "__main__":
    unittest.main()
