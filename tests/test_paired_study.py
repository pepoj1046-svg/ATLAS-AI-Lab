import unittest
from atlas.paired_study import run_paired
from atlas.profiles import chosen_profile

class StudyTests(unittest.TestCase):
    def test_profile_free_configuration(self):
        profile = chosen_profile()
        self.assertTrue(profile.endpoint.startswith("https://"))
        self.assertEqual(profile.model, "openai/gpt-oss-20b")
        self.assertLessEqual(profile.request_ceiling, 20)

    def test_paired_equal_requests(self):
        calls = []
        def mock(prompt, context):
            calls.append((prompt, context))
            return "0"
        result = run_paired(mock)
        self.assertEqual(result["requests"], 8)
        self.assertEqual(len(calls), 8)
        self.assertEqual([x[0] for x in calls[::2]], [x[0] for x in calls[1::2]])

    def test_limit_blocks_requests(self):
        def fail(*args):
            raise AssertionError("Never call")
        with self.assertRaises(ValueError):
            run_paired(fail, max_requests=7)

if __name__ == "__main__":
    unittest.main()
