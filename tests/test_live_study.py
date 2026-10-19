import os
import unittest
from unittest.mock import patch
from atlas.run_live_study import main


class LiveStudyEntryTests(unittest.TestCase):
    def test_missing_key_fails_before_model_calls(self):
        env = {"ATLAS_MODEL_ENDPOINT": "https://api.groq.com/openai/v1/chat/completions",
               "ATLAS_MODEL_NAME": "openai/gpt-oss-20b"}
        with patch.dict(os.environ, env, clear=True):
            with patch("atlas.run_live_study.ask_model") as mock:
                with self.assertRaises(SystemExit):
                    main()
                mock.assert_not_called()

    def test_wrong_endpoint_fails(self):
        env = {"ATLAS_MODEL_ENDPOINT": "https://example.net/chat/completions",
               "ATLAS_MODEL_NAME": "openai/gpt-oss-20b",
               "ATLAS_MODEL_API_KEY": "dummy"}
        with patch.dict(os.environ, env, clear=True):
            with patch("atlas.run_live_study.ask_model") as mock:
                with self.assertRaises(SystemExit):
                    main()
                mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
