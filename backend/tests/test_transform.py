import pytest
import pandas as pd
from transform.data_transformer import DataTransformer

@pytest.fixture
def transformer():
    return DataTransformer()

def test_clean_data(transformer):
    data = pd.DataFrame({
        'column_name': [1, 2, 2, -1, None],
        'key_column': ['A', 'B', 'C', 'A', 'D']
    })
    cleaned_data = transformer.clean_data(data)
    assert cleaned_data.isnull().sum().sum() == 0
    assert cleaned_data['column_name'].min() >= 0

def test_filter_data(transformer):
    data = pd.DataFrame({'column_name': [1, 2, 3, 4, 5]})
    filtered_data = transformer.filter_data(data, "column_name > 2")
    assert not filtered_data.empty
    assert (filtered_data['column_name'] > 2).all()

@patch('requests.get')
def test_enrich_data_with_api(mock_get, transformer):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"info": "enriched"}
    
    data = pd.DataFrame({'key_column': ['A', 'B']})
    enriched_data = transformer.enrich_data(data)
    assert 'external_data' in enriched_data.columns
    assert enriched_data['external_data'].iloc[0] == {"info": "enriched"}