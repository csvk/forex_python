import json
API_CREDS_FILE = 'D:/OneDrive/Studies/forex_python/api_creds.json'

# Load API credentials
with open(API_CREDS_FILE) as json_file:
    apicreds = json.load(json_file)

class defs():
    API_KEY = apicreds['API_KEY']
    ACCOUNT_ID = apicreds['ACCOUNT_ID']
    OANDA_URL = apicreds['OANDA_URL']

    SECURE_HEADER = {
        'Authorization': f'Bearer {API_KEY}'
}

import requests
import pandas as pd
import utils

class OandaAPI():

    def __init__(self):
        self.session = requests.Session()    

    def fetch_instruments(self):
        url = f"{defs.OANDA_URL}/accounts/{defs.ACCOUNT_ID}/instruments"
        response = self.session.get(url, params=None, headers=defs.SECURE_HEADER)
        return response.status_code, response.json()
    
    def get_instruments_df(self):
        code, data = self.fetch_instruments()
        if code == 200:
            df = pd.DataFrame.from_dict(data['instruments'])
            return df[['name', 'type', 'displayName', 'pipLocation', 'marginRate']]
        else:
            return None
    
    def save_instruments(self):
        df = self.get_instruments_df()
        if df is not None:
            df.to_pickle(utils.get_instruments_data_filename())

    def fetch_candles(self, pair_name, count, granularity):
        url = f"{defs.OANDA_URL}/instruments/{pair_name}/candles"

        params = dict(
            count = count,
            granularity = granularity,
            price = "MBA"
        )

        response = self.session.get(url, params=params, headers=defs.SECURE_HEADER)

        return response.status_code, response.json()


if __name__ == "__main__":
    api = OandaAPI()
    api.save_instruments()