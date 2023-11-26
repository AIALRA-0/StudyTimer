from datetime import datetime, timedelta
from flask import Flask, render_template, redirect, url_for, jsonify, request
from study_timer import StudyTimer
from block_hosts import block_sites, unblock_sites, read_blocked_sites

# 创建 Flask 应用实例，指定模板文件夹路径
app = Flask(__name__)
timer = StudyTimer()  # 创建 StudyTimer 实例
BLOCKED_SITES = read_blocked_sites()


@app.route('/')
def index():
    days = request.args.get('days', default=7, type=int)  # 获取天数参数，默认为7
    timer.load_data()  # 确保加载最新数据

    # 现在只获取请求的天数范围内的数据
    sorted_records = dict(sorted(timer.daily_records.items(), key=lambda x: x[0], reverse=True))
    limited_records = {date: sorted_records[date] for date in list(sorted_records)[:days]}

    formatted_records = {date: str(duration).split('.')[0] for date, duration in limited_records.items()}

    # 计算平均学习时间
    avg_7_days = calculate_average(timer.daily_records, 7)
    avg_30_days = calculate_average(timer.daily_records, 30)
    avg_365_days = calculate_average(timer.daily_records, 365)

    return render_template('index.html', records=formatted_records, avg_7_days=avg_7_days, avg_30_days=avg_30_days,
                           avg_365_days=avg_365_days)


def calculate_average(records, days):
    today = datetime.now().date()
    period_sum = timedelta()
    count = 0
    for i in range(days):
        current_date = (today - timedelta(days=i)).isoformat()
        if current_date in records:
            period_sum += records[current_date]
            count += 1
    if count > 0:
        average = period_sum / count
    else:
        average = timedelta(0)
    return str(average).split('.')[0]


@app.route('/start', methods=['GET', 'POST'])
def start_study_session():
    block_sites(BLOCKED_SITES)  # 使用 python-hosts 库屏蔽网站
    if request.method == 'POST':
        timer.start()
        return jsonify({'status': 'success', 'message': 'Study session started'})
    else:
        timer.start()
        return redirect(url_for('index'))


@app.route('/stop', methods=['GET', 'POST'])
def stop_study_session():
    session_duration = timer.stop()
    unblock_sites()  # 使用 python-hosts 库解除屏蔽
    timer.save_data()
    if request.method == 'POST':
        return jsonify({'status': 'success', 'message': 'Study session stopped', 'duration': str(session_duration)})
    else:
        return redirect(url_for('index'))


@app.route('/clear')
def clear():
    timer.clear_today()
    timer.save_data()
    return redirect(url_for('index'))
