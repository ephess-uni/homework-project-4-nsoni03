# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    return [datetime.strptime(date, "%Y-%m-%d").strftime("%d %b %Y") for date in old_dates]


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str) or not isinstance(n, int):
        raise TypeError
    start_datetime = datetime.strptime(start, "%Y-%m-%d")
    return [start_datetime + timedelta(days=val) for val in range(n)]


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    return [(datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=temp), value) for temp, value in enumerate(values)]


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    with open(infile) as f:
        filtered_lis=[]
        DictReader_obj = DictReader(f)
        for item in DictReader_obj:
            sample_dict={}
            day=datetime.strptime(item['date_returned'],'%m/%d/%Y')- datetime.strptime(item['date_due'],'%m/%d/%Y') 
            sample_dict["patron_id"]=item['patron_id']
            if(day.days>0):
                sample_dict["late_fees"]=round(day.days*0.25, 2)
                filtered_lis.append(sample_dict)
            else:
                sample_dict["late_fees"]=float(0)
                filtered_lis.append(sample_dict)
        agg_dict = {}
        for dict in filtered_lis:
            agg_dict[dict['patron_id']] = agg_dict.get(dict['patron_id'], 0) + dict['late_fees']
        final_list = [{'patron_id': key, 'late_fees': '{:.2f}'.format(value)} for key, value in agg_dict.items()]

    with open(outfile,"w", newline="") as file:
        writer = DictWriter(file, fieldnames=['patron_id', 'late_fees'])
        writer.writeheader()
        writer.writerows(final_list)


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
