# Time Zone Converter

## 📌 Description

This Python application allows users to easily convert time between different time zones. The application provides the following functionalities:

- Display the current time in any time zone
- Convert a specific time from one time zone to another
- Show the difference between time zones
- Provide information on daylight saving time (DST)

## 🛠 Requirements

To run the application, install the following libraries:

```sh
pip install pytz python-dateutil
```

## 🚀 How to Use

1. Run the application:
   ```sh
   python main.py
   ```
2. Select an option from the menu.
3. Follow the on-screen instructions to enter time zones and time.

## 📌 Code Example

```python
import pytz
from datetime import datetime
from dateutil import parser

zone = "Europe/Belgrade"
tz = pytz.timezone(zone)
current_time = datetime.now(pytz.UTC).astimezone(tz)
print(f"Current time in {zone}: {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
```

## 📋 Menu Options

1️⃣ **Display current time in a zone** – Enter a time zone and get the current time in that zone.
2️⃣ **Convert a specific time** – Enter a date and time in one zone and convert it to another zone.
3️⃣ **Show time zone difference** – View the difference in hours between two time zones.
4️⃣ **Daylight Saving Time information** – Find out if a time zone uses daylight saving time.
5️⃣ **Exit** – Exit the application.

## 📝 Author
**Bojana** – Developed the application in Python using `pytz` and `dateutil`.

## 📜 License

This project is open source and available under the MIT license.

