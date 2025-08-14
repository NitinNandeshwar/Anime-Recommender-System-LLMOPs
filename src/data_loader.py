import pandas as pd

class AnimeDataLoader:
    def __init__(self, original_csv:str,processed_csv:str):
        self.original_csv = original_csv
        self.processed_csv = processed_csv


    def load_and_process(self):
        """Load data from the specified CSV file."""
        try:
            df = pd.read_csv(self.original_csv,encoding='utf-8',on_bad_lines= 'skip').dropna()
            required_cols = {'Name' , 'Genres','sypnopsis'}

            missing =required_cols - set(df.columns)
            if missing:
                raise ValueError(f"Missing required columns: {missing} in CSV file {self.original_csv}")
            
            df['combined_info'] = ('Title: ' + df['Name'] + ' Overview' + 
                                   df['sypnopsis'] + ' Genres: ' + df['Genres'])
            
            df[['combined_info']].to_csv(self.processed_csv, index=False, encoding='utf-8')
            
            print(f"Data loaded successfully from {self.original_csv} and processed to {self.processed_csv}")

            return self.processed_csv
        
        except Exception as e:
            print(f"Error loading data: {e}")

