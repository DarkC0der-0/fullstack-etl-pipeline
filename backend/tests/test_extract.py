import pytest
from unittest.mock import patch
from extract.data_extractor import DataExtractor

@pytest.fixture
def extractor():
    return DataExtractor()

@patch('extract.data_extractor.requests.get')
def test_extract_from_api(mock_get, extractor):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"key": "value"}
    
    data = extractor.extract_from_api("https://api.example.com/data")
    assert data == {"key": "value"}

@patch('pandas.read_csv')
def test_extract_from_csv(mock_read_csv, extractor):
    mock_read_csv.return_value = pd.DataFrame({"column": [1, 2, 3]})
    
    data = extractor.extract_from_csv("path/to/file.csv")
    assert data is not None
    assert not data.empty

@patch('boto3.client')
def test_extract_from_s3(mock_boto3_client, extractor):
    mock_s3_client = mock_boto3_client.return_value
    mock_s3_client.get_object.return_value = {
        'Body': io.StringIO("column\n1\n2\n3")
    }

    data = extractor.extract_from_s3("bucket-name", "path/to/file.csv")
    assert data is not None
    assert not data.empty