import yfinance as yf
from datetime import datetime, timedelta

def fetch_stock_data(ticker):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=14*365)
    data = yf.download(ticker, start=start_date, end=end_date)
    data = data[['Close']].reset_index()
    data['dailyIncrease'] = data['Close'] / data['Close'].shift(1)
    data['dailyIncrease'] = data['dailyIncrease'].fillna(1)
    return data

def CompareStocks(stock1, stock2, threshold=0.005):
    omx30_data = {}
    omx30_data[stock1] = fetch_stock_data(stock1)
    omx30_data[stock2] = fetch_stock_data(stock2)
    print(f"Data fetched for {stock1} and {stock2}")

    choosing_lowest_value = 1
    switch_count_lowest = 0
    not_switch_count_lowest = 0
    last_chosen_stock_lowest = None

    for index, row in omx30_data[stock1].iterrows():
        if index + 1 < len(omx30_data[stock1]):
            increase_ticker1 = omx30_data[stock1].iloc[index]['dailyIncrease']
            increase_ticker2 = omx30_data[stock2].iloc[index]['dailyIncrease']

            if last_chosen_stock_lowest is None or abs(increase_ticker1 - increase_ticker2) >= threshold:
                chosen_stock = stock1 if increase_ticker1 < increase_ticker2 else stock2
            else:
                chosen_stock = last_chosen_stock_lowest

            next_increase = omx30_data[chosen_stock].iloc[index + 1]['dailyIncrease']
            
            if last_chosen_stock_lowest and chosen_stock != last_chosen_stock_lowest:
                next_increase -= 0.0018
                switch_count_lowest += 1
                choosing_lowest_value *= next_increase
            elif last_chosen_stock_lowest == chosen_stock:
                not_switch_count_lowest += 1

            last_chosen_stock_lowest = chosen_stock

    choosing_highest_value = 1
    switch_count_highest = 0
    not_switch_count_highest = 0
    last_chosen_stock_highest = None

    for index, row in omx30_data[stock1].iterrows():
        if index + 1 < len(omx30_data[stock1]):
            increase_ticker1 = omx30_data[stock1].iloc[index]['dailyIncrease']
            increase_ticker2 = omx30_data[stock2].iloc[index]['dailyIncrease']

            if last_chosen_stock_highest is None or abs(increase_ticker1 - increase_ticker2) >= threshold:
                chosen_stock = stock1 if increase_ticker1 > increase_ticker2 else stock2
            else:
                chosen_stock = last_chosen_stock_highest

            next_increase = omx30_data[chosen_stock].iloc[index + 1]['dailyIncrease']
            
            if last_chosen_stock_highest and chosen_stock != last_chosen_stock_highest:
                next_increase -= 0.0018
                switch_count_highest += 1
                choosing_highest_value *= next_increase
            elif last_chosen_stock_highest == chosen_stock:
                not_switch_count_highest += 1

            last_chosen_stock_highest = chosen_stock

    base_case_stock1 = (omx30_data[stock1]['dailyIncrease']).cumprod().iloc[-1]
    base_case_stock2 = (omx30_data[stock2]['dailyIncrease']).cumprod().iloc[-1]

    return {
        "highest_value": choosing_highest_value,
        "lowest_value": choosing_lowest_value,
        "base_case_stock1": base_case_stock1,
        "base_case_stock2": base_case_stock2,
        "switch_count_highest": switch_count_highest,
        "switch_count_lowest": switch_count_lowest,
        "not_switch_count_highest": not_switch_count_highest,
        "not_switch_count_lowest": not_switch_count_lowest
    }


# The rest of your code where you call CompareStocks for different pairs goes here


pairs = [
    ("ATCO-A.ST", "ATCO-B.ST"),
    ("SHB-A.ST", "SHB-B.ST"),
    ("ERIC-A.ST", "ERIC-B.ST"),
    ("VOLV-A.ST", "VOLV-B.ST"),
    # Additional pairs
    ("SEB-A.ST", "SEB-C.ST"),
    ("INVE-A.ST", "INVE-B.ST"),
    ("KINV-A.ST", "KINV-B.ST"),
]

thresholds = [0.005, 0.01, 0.015, 0.02, 0.025]  # Example thresholds
for threshold in thresholds:
    print(f"Testing with threshold: {threshold}")
    for pair in pairs:
        results = CompareStocks(pair[0], pair[1], threshold=threshold)

        print(f"Comparing {pair[0]} and {pair[1]} at threshold {threshold}")
        print(f"Lowest Value: {results['lowest_value']}, Switches: {results['switch_count_lowest']}, Not Switches: {results['not_switch_count_lowest']}")
        print("---")
    print("======")