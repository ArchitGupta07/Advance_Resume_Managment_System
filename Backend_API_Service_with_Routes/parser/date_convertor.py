# Define the start and end dates as strings

from datetime import datetime


def string_to_date(date_range):
    date_range = date_range.strip("-")
    start_date = date_range[0]
    end_date = date_range[1]

    # Parse the dates into datetime objects
    start_date_obj = datetime.strptime(start_date, "%b %Y")
    if end_date.lower() in ["present", "current"]:
        end_date_obj = datetime.now()
    else:
        end_date_obj = datetime.strptime(end_date, "%b %Y")

    # Calculate the difference in months
    months_diff = (end_date_obj.year - start_date_obj.year) * 12 + end_date_obj.month - start_date_obj.month

    # print("Duration in months:", months_diff)
    return months_diff


from datetime import datetime
import re

def to_date(start_date, end_date):

    start_date = re.sub(r"[\"'`’]" ," ", start_date )
    end_date = re.sub(r"[\"'`’]" ," ", end_date )

    # start_date, end_date = start_date.split(), end_date.split()

    # print(start_date, end_date)
    try:

        if len(start_date.split())==2:
        # Parse the dates into datetime objects
            start_date = start_date.split()
            start_date[0]=start_date[0][:3]
            if len(start_date[1])==2:
                start_date[1]= "20"+start_date[1]
            start_date = " ".join(start_date)
            # print(start_date)
            start_date_obj = datetime.strptime(start_date.title(), "%b %Y")
        else:
            start_date_obj = datetime.strptime(start_date.title(), "%Y")
            

        if len(end_date.split())==2:
            end_date = end_date.split()
            end_date[0]=end_date[0][:3]
            if len(end_date[1])==2:
                end_date[1]= "20"+end_date[1]
            end_date = " ".join(end_date)
            # print(end_date)
            end_date_obj = datetime.strptime(end_date.title(), "%b %Y")
        else:
            if end_date.lower() in ["present", "current"]:
                end_date_obj = datetime.now()
            else:
                end_date_obj = datetime.strptime(end_date.title(), "%Y")

        # Calculate the difference in months
        months_diff = (end_date_obj.year - start_date_obj.year) * 12 + end_date_obj.month - start_date_obj.month

        # print("Duration in months:", months_diff)
        return months_diff
    except ValueError:
        # print("Invalid date format. Please use a format like 'Jun 2022'.")
        return 0

# print(to_date('oct’11', 'jul’12'))


