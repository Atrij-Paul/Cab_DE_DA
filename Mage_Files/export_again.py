from mage_ai.data_preparation.repo_manager import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.mysql import MySQL
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

@data_exporter
def export_data_to_mysql(data, **kwargs) -> None:
    """
    Template for exporting data to a MySQL database.
    Specify your configuration settings in 'io_config.yaml'.
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    # Open a MySQL connection using the config file
    with MySQL.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        # Loop through the data dictionary and export each DataFrame to a separate table
        for key, value in data.items():
            df = DataFrame(value)
            print(f"Processing table: {key}")
            print(f"Number of rows in DataFrame: {len(df)}")
            
            # Ensure the DataFrame has more than 5 rows before exporting
            if len(df) > 5:
                table_name = 'cab_final_new.{}'.format(key)  # Replace with your actual database and table name
                loader.export(
                    df,
                    schema_name=None,  # Can specify the schema name if needed
                    table_name=table_name,
                    index=False,  # Specifies whether to include the index in the exported table
                    if_exists='replace',  # Specify resolution policy if table name already exists
                )
            else:
                print(f"DataFrame for table '{key}' has 5 or fewer rows and will not be exported.")
