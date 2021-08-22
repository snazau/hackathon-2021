import pandas as pd
import os
import time
import datetime

def get_bad_transaction_list(label_path, label_id):
    label_csv = pd.read_csv(label_path, sep=",")
    bad_transactions_frame = label_csv[label_csv['target_id'] == label_id]

    bad_transactions_list = set()
    for index, row in bad_transactions_frame.iterrows():
        temp_transactions = str(row['Номер эВСД оформленного с нарушениями'])
        temp_transactions = temp_transactions.replace(',', '')
        temp_transactions = temp_transactions.split(' ')
        for transaction in temp_transactions:
            if transaction.isdigit():
                bad_transactions_list.add(int(transaction))

    return bad_transactions_list


def find_bad_times(label_path, time_path, label_id, debug=False):
    bad_transactions_list = get_bad_transaction_list(label_path, label_id)
    if debug:
        print(f'Number of bad transactions: {len(bad_transactions_list)}')

    time_csv = pd.read_csv(time_path, sep=";", encoding="cp1251")
    time_csv = time_csv.sort_values('id')

    bad_ids = []
    for index, row in time_csv.iterrows():
        date_from = row['cert_date']
        date_to = row['repaid_cert_date']
        id = row['id']

        if id in bad_transactions_list:
            if debug:
                print('Already found')
                continue

        if not isinstance(date_to, str):
            bad_ids.append(bad_ids)
            if debug:
                print(f'Id: {id}')
                print('Nan in repaid_cert_date')
        else:
            seconds_from = time.mktime(datetime.datetime.strptime(date_from[:-3], "%Y/%m/%d %H:%M:%S.%f").timetuple())
            seconds_to = time.mktime(datetime.datetime.strptime(date_to[:-3], "%Y/%m/%d %H:%M:%S.%f").timetuple())
            hours = (seconds_to - seconds_from) / 3600

            if abs(hours - row['transit_time_hour']) >= 24:
                if debug:
                    bad_ids.append(bad_ids)
                    print(f'Id: {id}')
                    print('Big difference with transit_time_hour.')

            # Maximum time
            if hours > 2160:
                if debug:
                    bad_ids.append(bad_ids)
                    print(f'Id: {id}')
                    print('Too long.')

            # Minimum time
            if hours < 1:
                if debug:
                    bad_ids.append(bad_ids)
                    print(f'Id: {id}')
                    print('Too short.')

    return bad_ids


if __name__ == "__main__":
    label_dir = os.path.join(os.path.dirname(__file__), 'data')
    time_dir = os.path.join(os.path.dirname(__file__), 'data')

    label_path = os.path.join(label_dir, 'labels_pretty.csv')
    time_path = os.path.join(time_dir, "Certificate_2020_ds_0.txt")

    bad_ids = find_bad_times(label_path, time_path, 4, debug=True)
