from django.shortcuts import render
import pyodbc
import pandas as pd
import time
from django.conf import settings
import plotly.express as px
from django.shortcuts import render
import requests
import json

def connsql(request):
    geocoded_result = []
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    page_number = request.GET.get('page', 1)  # Default page number is 1

    start_time = time.time()  # Start measuring time

    conn = pyodbc.connect('Driver={sql server};'
                          'Server=servername;'
                          'Database=databasename;'
                          'Trusted_Connection=yes;'
                          )

    cursor = conn.cursor()

    # Count the total number of records within the specified date range
    count_query = "SELECT COUNT(*) FROM tablename"
    where_clause = ""
    params = []

    if start_date and end_date:
        where_clause = " WHERE ISSUE_DATE BETWEEN ? AND ?"
        params.extend([start_date, end_date])

    # Add condition to filter out null values
    if where_clause:
        where_clause += " AND Latitude IS NOT NULL AND Longitude IS NOT NULL"

    cursor.execute(count_query + where_clause, params)
    total_records = cursor.fetchone()[0]

    # Calculate pagination parameters dynamically
    items_per_page = min(200000, total_records)  # Limit to 200,000 records
    offset = (int(page_number) - 1) * items_per_page

    # Construct the main query
    query = "SELECT VIOLATION_CODE, ISSUE_DATE, Latitude, Longitude FROM tablename"

    if where_clause:
        query += where_clause

    query += f" ORDER BY ISSUE_DATE OFFSET {offset} ROWS FETCH NEXT {items_per_page} ROWS ONLY"

    # Execute the main query
    cursor.execute(query, params)
    result = cursor.fetchall()

    # Fetch available years from your data
    available_years_query = "SELECT MIN(YEAR(ISSUE_DATE)) AS min_year, MAX(YEAR(ISSUE_DATE)) AS max_year FROM tablename WHERE YEAR(ISSUE_DATE) BETWEEN 2018 AND 2024"
    available_years_cursor = conn.cursor()
    available_years_cursor.execute(available_years_query)
    available_years_result = available_years_cursor.fetchone()

    min_year = available_years_result.min_year
    max_year = available_years_result.max_year
    available_years = list(range(min_year, max_year + 1))

    # Format the date range string
    date_range_str = f"{start_date} to {end_date}" if start_date and end_date else "No date range specified"

    for row in result:
        violation_code = row.VIOLATION_CODE
        issue_date = row.ISSUE_DATE
        latitude = row.Latitude if row.Latitude is not None else 'null'
        longitude = row.Longitude if row.Longitude is not None else 'null'

        geocoded_result.append({
            'violation_code': violation_code,
            'coordinates': (latitude, longitude),
            'issue_date': issue_date,
        })

    conn.close()

    end_time = time.time()  # End measuring time
    run_time = end_time - start_time  # Calculate run time

    print("Run time:", run_time, "seconds")  # Print run time to server console

    return render(request, 'map200.html', {'sqlserverconn': geocoded_result,
                                         'available_years': available_years,
                                         'min_year': min_year,
                                         'max_year': max_year,
                                         'total_records': total_records,
                                         'date_range': date_range_str})
