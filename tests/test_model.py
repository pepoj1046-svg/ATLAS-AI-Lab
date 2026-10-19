import os
import unittest
from unittest.mock import patch
from atlas.model import ask_model, ModelUnavailable
from atlas.llm_experiment import evaluate


class ModelTests(unittest.TestCase):
    def test_disabled_without_credentials(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ModelUnavailable):
                ask_model("1+1")

    def test_rejects_local_endpoint(self):
        with patch.dict(os.environ, {"ATLAS_MODEL_ENDPOINT": "http://localhost:9999",
                                      "ATLAS_MODEL_NAME": "demo",
                                      "ATLAS_MODEL_API_KEY": "dummy"}, clear=True):
            with self.assertRaises(ModelUnavailable):
                ask_model("1+1")

    def test_comparison_is_mockable_and_no_network_needed(self):
        with patch("atlas.llm_experiment.ask_model", side_effect=["41", "104", "31"]):
            result = evaluate()
        self.assertEqual(result["correct"], 2)
        self.assertEqual(result["total"], 3)


if __name__ == "__main__":
    unittest.main()
