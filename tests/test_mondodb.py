import unittest
from unittest.mock import MagicMock, patch

from src.mondodb import (close_db_client, create_db_client, get_from_mongodb,
                         load_to_mongodb)
from src.patient_model import Patient


class TestMondodbOperations(unittest.TestCase):
    @patch('src.mondodb.MongoClient')
    def test_create_db_client(self, mock_client):
        db = create_db_client()
        mock_client.assert_called_once()
        self.assertIsNotNone(db)

    @patch('src.mondodb.MongoClient')
    def test_close_db_client(self, mock_client):
        db = create_db_client()
        close_db_client(db)
        db.client.close.assert_called_once()

    @patch('src.mondodb.MongoClient')
    def test_load_to_mongodb(self, mock_client):
        mock_db = MagicMock()
        mock_client.return_value = MagicMock(smartNationAI=mock_db)
        patient = Patient(patient_id="123", age="30", gender="male")
        load_to_mongodb(patient)
        mock_db.patients.insert_one.assert_called_once_with(patient.dict())

    @patch('src.mondodb.MongoClient')
    def test_get_from_mongodb(self, mock_client):
        mock_db = MagicMock()
        mock_client.return_value = MagicMock(smartNationAI=mock_db)
        mock_db.patients.find_one.return_value = {"patient_id": "123", "age": "30", "gender": "male"}
        patient_data = get_from_mongodb("123")
        mock_db.patients.find_one.assert_called_once_with({"patient_id": "123"})
        self.assertEqual(patient_data, {"patient_id": "123", "age": "30", "gender": "male"})

    @patch('src.mondodb.MongoClient')
    def test_get_from_mongodb_nonexistent_id(self, mock_client):
        mock_db = MagicMock()
        mock_client.return_value = MagicMock(smartNationAI=mock_db)
        mock_db.patients.find_one.return_value = None
        patient_data = get_from_mongodb("nonexistent_id")
        mock_db.patients.find_one.assert_called_once_with({"patient_id": "nonexistent_id"})
        self.assertIsNone(patient_data)

if __name__ == '__main__':
    unittest.main()
