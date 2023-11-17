import datetime
import json


def save_mondays_thursdays_to_json(year, file_path):
    # Generate the dates
    date = datetime.date(year, 11, 20)
    mondays_thursdays = []
    while date.year == year:
        if date.weekday() in (0, 3):  # 0 for Monday, 3 for Thursday
            mondays_thursdays.append(date.isoformat())  # Store date as string
        date += datetime.timedelta(days=1)

    # Prepare the data for JSON
    data = {"DATES": mondays_thursdays}

    # Write to JSON file
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)


if __name__ == "__main__":
    year = 2023
    file_path = r"resources\available.json"
    save_mondays_thursdays_to_json(year, file_path)
