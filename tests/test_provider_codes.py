import io
import os
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from atlas.model import ask_model, ModelUnavailable

class ProviderCodeTests(unittest.TestCase):
    def test_known_error_code(self):
        payload=b'{"error":{"code":"model_permission_blocked_project","message":"do not disclose"}}'
        def forbidden(*args,**kwargs):
            raise HTTPError("https://api.groq.com",403,"Forbidden",None,io.BytesIO(payload))
        env={"ATLAS_MODEL_ENDPOINT":"https://api.groq.com/openai/v1/chat/completions",
             "ATLAS_MODEL_NAME":"openai/gpt-oss-20b","ATLAS_MODEL_API_KEY":"secret"}
        with patch.dict(os.environ,env,clear=True),patch("atlas.model.urlopen",side_effect=forbidden):
            with self.assertRaises(ModelUnavailable) as caught:
                ask_model("2+2")
        self.assertIn("model_permission_blocked_project",str(caught.exception))
        self.assertNotIn("secret",str(caught.exception))
        self.assertNotIn("do not disclose",str(caught.exception))

    def test_unknown_code_is_redacted(self):
        payload=b'{"error":{"code":"secret_revealing_value","message":"private"}}'
        def forbidden(*args,**kwargs):
            raise HTTPError("https://api.groq.com",403,"Forbidden",None,io.BytesIO(payload))
        env={"ATLAS_MODEL_ENDPOINT":"https://api.groq.com/openai/v1/chat/completions",
             "ATLAS_MODEL_NAME":"openai/gpt-oss-20b","ATLAS_MODEL_API_KEY":"secret"}
        with patch.dict(os.environ,env,clear=True),patch("atlas.model.urlopen",side_effect=forbidden):
            with self.assertRaises(ModelUnavailable) as caught:
                ask_model("2+2")
        self.assertIn("[unclassified]",str(caught.exception))
        self.assertNotIn("secret_revealing_value",str(caught.exception))
