import os
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from atlas.model import ask_model, ModelUnavailable

class ErrorDiagnosticsTests(unittest.TestCase):
    def test_403_redacts_details(self):
        env={"ATLAS_MODEL_ENDPOINT":"https://api.groq.com/openai/v1/chat/completions",
             "ATLAS_MODEL_NAME":"openai/gpt-oss-20b","ATLAS_MODEL_API_KEY":"secret-test"}
        def forbidden(*a,**k):
            raise HTTPError("https://api.groq.com/openai/v1/chat/completions",403,"Sensitive payload",None,None)
        with patch.dict(os.environ,env,clear=True), patch("atlas.model.urlopen",side_effect=forbidden):
            with self.assertRaises(ModelUnavailable) as caught:
                ask_model("1+1")
        self.assertIn("403",str(caught.exception))
        self.assertNotIn("secret-test",str(caught.exception))
        self.assertNotIn("Sensitive payload",str(caught.exception))

if __name__=="__main__":
    unittest.main()
