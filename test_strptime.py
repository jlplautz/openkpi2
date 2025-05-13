from datetime import datetime

# Example string
date_str = '2025-03-31 04:45'

# Convert string to datetime object
date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M')

print(date_obj)  # Output: 2025-03-31 04:45:00
print(type(date_obj))  # Output: <class 'datetime.datetime'>