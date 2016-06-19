# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 21:40:34 2016

@author: psukumar
"""
import csv
from datetime import datetime
import re

def price_mean(*args):
    """ Computes mean for a variable number of float arguments """
    return round(float(sum(args))/len(args),2)
    
def is_id(order_text):
    """ Checks if incoming string is of id format """
    try:
        int(order_text)
        return True
    except:
        return False
        
 
def is_float(val):
    """ Checks if incoming string is of float format """
    try:
        float(val)
        return True
    except:
        return False
        
def is_instacart_url(url):
    """ Checks if url has the correct format """
    pattern = re.compile("http://www.insacart.com")
    return True if pattern.match(url) else False

def is_date_YYYYMMDD(date_string):
    """ Checks if date format is correct """
    try:
        datetime.strptime(date_string, '%Y%m%d')
        return True
    except ValueError:
        return False
    

def transform_row(inrow):
    """
    Transforms a single row into source to
    corresponding target row.
    Error messages if any are cumulative in the output row
    Invlid url's do not appear
   """
    error_msg  = [] 
    if len(inrow) < 7:
        error_msg.append("Missing field")
    elif len(inrow) > 7:
        error_msg.append("Extra field")
          
    orderid_dt = inrow[0].strip().split(":")
    
    try:
        order_id = orderid_dt[0]
    except:
        order_id = ""
        
    try:    
        order_date = orderid_dt[1]  
    except:
        order_date = ""

    user_id = inrow[1].strip()
    item_price_1 = inrow[2].strip() or 0
    item_price_2 = inrow[3].strip() or 0 
    item_price_3 = inrow[4].strip() or 0
    item_price_4 = inrow[5].strip() or 0
    start_page_url = inrow[6]
    can_avg = True
            
    if not is_id(order_id):
        error_msg.append("Invalid order_id")
        
    if not is_id(user_id):
        error_msg.append("Invalid user_id")
        
    if not is_date_YYYYMMDD(order_date):
        error_msg.append("Invalid order_date")
                    
    if not is_float(item_price_1):
        error_msg.append("Invalid item_price_1")
        can_avg = False
    else:
        item_price_1 = float(item_price_1)
            
    if not is_float(item_price_2):
        error_msg.append("Invalid item_price_2")
        can_avg = False
    else:
        item_price_2 = float(item_price_2)
        
    if not is_float(item_price_3):
        error_msg.append("Invalid item_price_3")
        can_avg = False
    else:
        item_price_3 = float(item_price_3)
        
    if not is_float(item_price_4):
        error_msg.append("Invalid item_price_4")
        can_avg = False
    else:
        item_price_4 = float(item_price_4)
    
    if not is_instacart_url(start_page_url):
        error_msg.append("Invalid URL")
        start_page_url = ""
        
    if can_avg:
        avg_item_price = str(price_mean(item_price_1, item_price_2, 
                                        item_price_3, item_price_4))
    else:
        avg_item_price = "" 
        
    return order_id, order_date, user_id, avg_item_price, start_page_url, \
            "|".join(error_msg)

    
    
def parser(input_file,output_file): 
    """ Parses input file line by line """
    with open(input_file) as ifile:
        order_data = csv.reader(ifile, delimiter='\t')
        next(order_data,None) # Skip Header
        with open(output_file,"wb") as ofile:
            out_data = csv.writer(ofile, delimiter='\t', 
                                  quoting = csv.QUOTE_NONE)
            for row in order_data:
                #print row,len(row)
                out_data.writerow(transform_row(row))
                
    
    
if __name__ == "__main__":
    input_file = "scripting_challenge_input_file.txt"
    output_file = "scripting_challenge_output_file.txt"
    print("Processing input file {0}".format(input_file))
    parser(input_file, output_file)
    print("Output file created at {0}".format(output_file))