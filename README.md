# habit-tracker-python
This project is a simple habit tracking backend application developed as part of the
OOFPP course.  
It allows users to create habits, track their completion, and analyze streaks using a
command line interface (CLI).

The focus of the project is on clean structure, object-oriented design, and functional
analytics, not on a graphical interface.

---

## Features

- Create and delete habits
- Support for daily and weekly habits
- Check off habits via the CLI
- Store data persistently using SQLite
- Analyze longest streaks per habit and across all habits
- Load sample data (fixtures) for testing and demonstration


## Installation & Setup

To install and run the Habit Tracker, follow these steps:


1. Clone or download the project from GitHub to your computer.
2. Make sure Python is installed

Check your Python version:
```bash
python3 --version
```

Required:
- Python 3.7 or higher
(Latest test with Python 3.13)

If Python is not installed, download it from:
https://www.python.org/downloads/


3. Create a virtual environment

Inside the project folder, run:
```bash
python3 -m venv .venv
```

Activate the virtual environment:

macOS / Linux
```bash
source .venv/bin/activate
```

Windows
```bash
.venv\Scripts\activate
```

You should now see (.venv) in your terminal.


4. Install dependencies

With the virtual environment activated:
```bash
pip install -r requirements.txt
```

This installs:
- click (CLI handling)
- pytest (testing)


5. Initialize the application

Create the SQLite database:
```bash
python3 -m habit_tracker.cli init
```


6. (Optional) Load sample data

To generate example habits and check-offs for testing:
```bash
python3 -m habit_tracker.cli load-fixtures
```
This creates several weeks of sample check-off data with different periodicity.


7. Run the application

You can now use the habit tracker via the CLI.

Example commands:
```bash
# Initialize database
python3 -m habit_tracker.cli init

# Load sample data
python3 -m habit_tracker.cli load-fixtures

# List all habits
python3 -m habit_tracker.cli list

# List habits by periodicity
python3 -m habit_tracker.cli list-by daily
python3 -m habit_tracker.cli list-by weekly

# Create a new habit
python3 -m habit_tracker.cli create "Yoga" --periodicity weekly
python3 -m habit_tracker.cli create "Meditation" --periodicity daily

# Check off a habit
python3 -m habit_tracker.cli check "Yoga"

# Analyze longest streak across all habits
python3 -m habit_tracker.cli analyze all

# Analyze longest streak for a specific habit
python3 -m habit_tracker.cli analyze habit "Yoga"

# Delete a habit
python3 -m habit_tracker.cli delete "Yoga"
```

## Testing

```bash
python -m pytest
```

## Notes
- The database file is created in the project folder `habits.db`
- Periodicity supports: `daily`, `weekly`


Enjoy testing my first Python "Application":)
