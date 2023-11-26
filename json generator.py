import json
from datetime import datetime, timedelta
import random

json_path = "study_data.json"


def generate_study_data(n_days):
    end_date = datetime.now()
    data = {}

    for i in range(n_days):
        current_date = end_date - timedelta(days=i)
        date_str = current_date.strftime("%Y-%m-%d")

        # 生成随机时间，这里假设学习时间不超过 12 小时
        hours = random.randint(0, 11)
        minutes = random.randint(0, 59)
        seconds = random.randint(0, 59)
        microseconds = random.randint(0, 999999)

        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{microseconds:06d}"
        data[date_str] = time_str

    with open(json_path, "w") as file:
        json.dump(data, file, indent=4)


# 调用函数生成示例数据（例如7天）
generate_study_data(365)
