from datetime import datetime, timedelta
import json
import os


class StudyTimer:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.current_session_duration = timedelta(0)
        self.total_time = timedelta(0)
        self.daily_records = {}

    def start(self):
        self.start_time = datetime.now()
        print(f"Study session started at {self.start_time}")

    def stop(self):
        if self.start_time:
            self.end_time = datetime.now()
            session_duration = self.end_time - self.start_time
            self.current_session_duration = session_duration  # 记录当前会话持续时间
            self.total_time += session_duration
            self._record_session(session_duration)
            self.start_time = None
            return session_duration
        else:
            print("No study session is currently active.")
            return timedelta(0)

    def _record_session(self, session_duration):
        date_key = datetime.now().date().isoformat()
        if date_key in self.daily_records:
            self.daily_records[date_key] += session_duration
        else:
            self.daily_records[date_key] = session_duration

    def show_weekly_summary(self):
        print("Weekly Study Time Summary:")
        today = datetime.now().date()
        for i in range(7):
            date_key = (today - timedelta(days=i)).isoformat()
            if date_key in self.daily_records:
                print(f"{date_key}: {self.daily_records[date_key]}")
            else:
                print(f"{date_key}: No record")

    def save_data(self):
        with open("study_data.json", "w") as file:
            json_data = {key: str(value) for key, value in self.daily_records.items()}
            json.dump(json_data, file, indent=4)

    def load_data(self):
        if os.path.exists("study_data.json"):
            with open("study_data.json", "r") as file:
                json_data = json.load(file)
                for key, value in json_data.items():
                    hours, minutes, seconds = map(float, value.split(':'))
                    self.daily_records[key] = timedelta(hours=hours, minutes=minutes, seconds=seconds)

    def clear_today(self):
        date_key = datetime.now().date().isoformat()
        if date_key in self.daily_records:
            del self.daily_records[date_key]


if __name__ == '__main__':
    # Example of using the StudyTimer
    timer = StudyTimer()
    timer.load_data()  # Load existing data
    timer.start()  # Start a study session
    # ... time passes ...
    timer.stop()  # End the study session
    timer.show_weekly_summary()  # Show the weekly summary
    timer.save_data()  # Save the data to a file
