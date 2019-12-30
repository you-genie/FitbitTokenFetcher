# Fitbit Analyzer

This project consists of 2 parts. Both are python jupyter notebook files.

## TokenFetcher
---
Fetch tokens from Fitbit. 
* TOKEN_F_NAME is the name token will be saved. Also used in datafetcher, so change them both. Currently its `data/auth.json`
* CLIENT_ID is the client id given by dev.fitbit.com.
* CLIENT_SECRET is the client secret given by dev.fitbit.com. 
* REDIRECT_URI is the uri which should be the SAME ONE registered in dev.fitbit.com application. To change this, REDIRECT_URI value should be https://your.code.running.address/auth strictly. Change dev.fitbit.com application's redirect_uri value to modify this value.

### token fetching steps
1. run ALL TokenFetcher notebook (including the top)
2. GOTO https://fitbit.run-us-west1.goorm.io/
3. press add_user button (which will direct you to fitbit auth page)
4. press logout button to proceed (YOU SHOULD NOT CHANGE THIS PART), which will open a new window of signing out.
5. press next button to proceed, which will direct you to the main / page.

## DataFetcher
---
Fetching data from Fitbit, using TOKEN_F_NAME
* TOKEN_F_NAME is the name token will be saved. Currently its `data/auth.json`
* CLIENT_ID, CLIENT_SECRET is the client id & secret given by dev.fitbit.com
* you don't need to run the test code

### data fetching steps
run all DataFetcher notebook
1. `token_dict` contains the token value, `get_token` will load the data/auth.json to doken_dict
2. `get_id_queue` will load the tokens to id_queue, which are token queue containing tokens **loaded from** TokenFetcher
3. `run_queue` is the timely threading module (set time seconds / dealing with queue actions here)
4. `run_queue` will operate `update_all_data`, which fetches _intraday data, activity data, sleep data_ from fitbit. **modify this part to change the dataset fetched.**
