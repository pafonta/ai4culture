import json
import requests
import datetime
import argparse


#api_token = 'pQdnG7QPbTD2KhZh'


parser = argparse.ArgumentParser(usage="event_search.py event_location start_date end_date")
parser.add_argument("event_location", type = str, help = "assign event location, such as New-York-City")
parser.add_argument("start_date", type = str, help = "assign event start date <yyyymmdd>, such as 20150101")
parser.add_argument("end_date", type = str, help = "assign event end date <yyyymmdd>, such as 20150131")
args = parser.parse_args()

def get_event(user_key, event_location, start_date, end_date, event_features, fname):
    data_lst = [] # output
    start_year = int(start_date[0:4])
    start_month = int(start_date[4:6])
    start_day = int(start_date[6:])

    end_year = int(end_date[0:4])
    end_month = int(end_date[4:6])
    end_day = int(end_date[6:])

    start_date = datetime.date(start_year, start_month, start_day)
    end_date = datetime.date(end_year, end_month, end_day)
    step = datetime.timedelta(days=1)

    while start_date <= end_date:

        date = str(start_date.year)
        if start_date.month < 10:
            date += '0' + str(start_date.month)
        else:
            date += str(start_date.month)

        if start_date.day < 10:
            date += '0' + str(start_date.day)
        else:
            date += str(start_date.day)
            date += "00"
            date += "-"	+ date


        url = "http://api.eventful.com/json/events/search?"
        url += "&app_key=" + user_key
        url += "&location=" + event_location
        # url += "&keyword="+ "music"
        url += "&date=" + date
        url += "&page_size=250"
        url += "&sort_order=popularity"
        url += "&sort_direction=descending"

        data = requests.get(url).json()
        # print(data)

        try:
            for i in range(len(data["events"]["event"])):
                data_dict = {}
                for feature in event_features:
                    data_dict[feature] = data["events"]["event"][i][feature]
                    data_lst.append(data_dict)
                print(data_dict)
        except:
            pass

        start_date += step

    file = open(fname, "w")

    # write the table head
    lst2 = []
    lst2.extend(event_features)
    table_header = ",".join(lst2) + "\n"
    file.write(table_header)

    # write the data
    for i in range(len(data_lst)):
    	lst2 = []
    	for feature in event_features:
    		lst2.append(str(data_lst[i][feature]).replace(",", " "))
    	file.write(",".join(lst2) + "\n")
    file.close()

def main():
    user_key = "pQdnG7QPbTD2KhZh"
    # event_location = "Geneva"
    # start_date = "20180701"
    # end_date = "20180703"
    event_location = args.event_location.replace("-"," ")
    start_date = args.start_date
    end_date = args.end_date
    event_features = ["latitude","longitude", "start_time", "stop_time", "all_day"]
    event_features += ["id","title","description","city_name", "region_name", "postal_code"]
    event_fname = "events.csv"

    get_event(user_key, event_location, start_date, end_date, event_features, event_fname)


if __name__ == '__main__':
    main()
