import datetime


def convert_seconds_to_timestamp(seconds):
    # Convert seconds to a timedelta object
    td = datetime.timedelta(seconds=seconds)

    # Extract hours, minutes, seconds, and milliseconds
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = td.microseconds // 1000

    # Format the timestamp
    timestamp = f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"
    return timestamp


def main():
    # Example usage
    seconds = 3661.123  # Example float value
    timestamp = convert_seconds_to_timestamp(seconds)
    print(timestamp)  # Output: 01:01:01.123


if __name__ == '__main__':
    main()
