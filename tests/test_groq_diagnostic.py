import os
import unittest
from unittest.mock import patch
from atlas.groq_diagnostic import main

class DiagnosticTests(unittest.TestCase):
    def test_success_redacts_answer(self):
        env={"ATLAS_MODEL_ENDPOINT":"https://api.groq.com/openai/v1/chat/completions",
             "ATLAS_MODEL_NAME":"openai/gpt-oss-20b","ATLAS_MODEL_API_KEY":"dummy"}
        with patch.dict(os.environ,env,clear=True),patch("atlas.groq_diagnostic.ask_model",return_value="4") as ask:
            with patch("builtins.print") as printed:
                main()
                printed.assert_called_once()
                ask.assert_called_once()

    def test_missing_secret_fails_before_request(self):
        env={"ATLAS_MODEL_ENDPOINT":"https://api.groq.com/openai/v1/chat/completions",
             "ATLAS_MODEL_NAME":"openai/gpt-oss-20b"}
        with patch.dict(os.environ,env,clear=True),patch("atlas.groq_diagnostic.ask_model") as ask:
            with self.assertRaises(SystemExit):
                main()
            ask.assert_not_called()
