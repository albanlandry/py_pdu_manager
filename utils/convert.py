from PyQt6.QtCore import QTime

def str_to_qtime(time_str):
    # Ensure the input string is in HHmm format and is 4 characters long
    if len(time_str) != 4 or not time_str.isdigit():
        raise ValueError("Time string must be in 'HHmm' format and 4 digits long")

    # Extract hours and minutes from the string
    hour = int(time_str[:2])
    minute = int(time_str[2:])

    # Create QTime object
    time = QTime(hour, minute)

    # Check if the QTime object is valid
    if not time.isValid():
        raise ValueError("Invalid time string")

    return time
