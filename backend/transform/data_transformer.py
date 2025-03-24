import pandas as pd
import requests

class DataTransformer:
    def __init__(self, reference_data_path=None, reference_api_url=None):
        self.reference_data = pd.read_csv(reference_data_path) if reference_data_path else None
        self.reference_api_url = reference_api_url

    def clean_data(self, data):
        # Drop duplicates
        data = data.drop_duplicates()

        # Handle missing values
        data = data.dropna()  # Alternatively, you can fill missing values using data.fillna()

        # Handle invalid data (e.g., negative values in a column that should only have positive values)
        data = data[(data['column_name'] >= 0)]  # Replace 'column_name' with actual column name

        return data

    def filter_data(self, data, condition):
        # Apply business rules for filtering
        filtered_data = data.query(condition)  # Example condition: "column_name > 0"
        return filtered_data

    def enrich_data(self, data):
        if self.reference_data is not None:
            # Join with reference data
            enriched_data = data.merge(self.reference_data, on='key_column', how='left')  # Replace 'key_column' with actual key column
        elif self.reference_api_url is not None:
            # Enrich data by joining with external API
            enriched_data = data.copy()
            enriched_data['external_data'] = enriched_data['key_column'].apply(self.fetch_external_data)  # Replace 'key_column' with actual key column
        else:
            enriched_data = data

        return enriched_data

    def fetch_external_data(self, key):
        try:
            response = requests.get(f"{self.reference_api_url}/{key}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed for key {key}: {e}")
            return None

# Example usage
if __name__ == "__main__":
    transformer = DataTransformer(reference_data_path="path/to/reference.csv", reference_api_url="https://api.example.com/data")

    # Sample data
    data = pd.DataFrame({
        'column_name': [1, 2, 2, -1, None],
        'key_column': ['A', 'B', 'C', 'A', 'D']
    })

    # Clean data
    cleaned_data = transformer.clean_data(data)
    print("Cleaned Data:")
    print(cleaned_data)

    # Filter data
    filtered_data = transformer.filter_data(cleaned_data, "column_name > 0")
    print("Filtered Data:")
    print(filtered_data)

    # Enrich data
    enriched_data = transformer.enrich_data(filtered_data)
    print("Enriched Data:")
    print(enriched_data)