import unittest
from unittest.mock import MagicMock, patch

from src.patient_model import Patient
from src.rag_chain_executor import execute_rag_for_doc, format_llm_response


class TestRAGChainExecutor(unittest.TestCase):

    @patch('src.rag_chain_executor.open', new_callable=unittest.mock.mock_open, read_data='mocked data')
    @patch('src.rag_chain_executor.yaml.safe_load')
    @patch('src.rag_chain_executor.load_llm')
    @patch('src.rag_chain_executor.Simple_RAG')
    def test_execute_rag_for_doc_success(self, mock_simple_rag, mock_load_llm, mock_yaml_load, mock_open):
        mock_yaml_load.return_value = {'llm': 'mock_llm', 'ner_prompts': {'test_key': {'path_retrieve_context': 'mock_path_context', 'path_query_llm': 'mock_path_query'}}}
        mock_load_llm.return_value = 'mocked_llm'
        mock_simple_rag_instance = MagicMock()
        mock_simple_rag_instance.invoke_rag.return_value = 'mocked_response'
        mock_simple_rag.return_value = mock_simple_rag_instance

        patient = execute_rag_for_doc('patient_id', 'config_path')
        self.assertIsInstance(patient, Patient)
        mock_simple_rag_instance.invoke_rag.assert_called_once()

    @patch('src.rag_chain_executor.open', side_effect=FileNotFoundError)
    def test_execute_rag_for_doc_failure(self, mock_open):
        with self.assertRaises(FileNotFoundError):
            execute_rag_for_doc('patient_id', 'invalid_config_path')

    def test_format_llm_response_success(self):
        self.assertEqual(format_llm_response('allergies', '[{"allergy": "Peanuts"}]'), [{"allergy": "Peanuts"}])
        self.assertEqual(format_llm_response('diagnoses', '["Diagnosis1", "Diagnosis2"]'), ["Diagnosis1", "Diagnosis2"])
        self.assertEqual(format_llm_response('medications', 'None'), None)

    def test_format_llm_response_failure(self):
        self.assertIsNone(format_llm_response('allergies', None))
        self.assertEqual(format_llm_response('allergies', 'invalid_json'), [])

if __name__ == '__main__':
    unittest.main()
