from flask import Flask, request, redirect
from db import init_session
import pandas as pd

session, engine = init_session()

app = Flask(__name__, static_url_path='/static/')

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "Missing file"

    f = request.files['file']
    if f.filename == '':
        return "No file selected"
    data = pd.read_csv(f)
    #filter out any non 2019 data
    data['date'] = pd.to_datetime(data['date'])
    data = data[data['date'].dt.year == 2019]
    try:
        data.to_sql('daily_agg_2019', engine, if_exists='append', index=False)
    except:
        return """File could not be uploaded to the database,
                this file might contain duplicates or has been uploaded previously."""
    return "Uploaded. Nice" 

@app.route('/monthly')
def monthly():
    data = pd.read_sql('daily_agg_2019', engine, parse_dates=['date'])
    if not len(data):
        return "[]"
    #using month_year col instead of pd.grouper to keep friendly grouping labels
    data['month_year'] = pd.to_datetime(data['date']).dt.to_period('M')
    data['month_year'] = data['month_year'].dt.strftime('%Y-%m')
    result = data.groupby(['month_year', 'dog_id'], as_index=False).sum()
    return result.to_json(orient='records')

@app.route('/mouth')
def mouth():
    data = pd.read_sql('daily_agg_2019', engine, parse_dates=['date'])
    if not len(data):
        return "[]"
    data['mouth_score'] = data.apply(
        lambda row: 2*row.eat_score + 0.5*row.drink_score + row.chew_score, axis=1)
    return data.to_json(orient='records')

@app.route('/jumpsniffavg')
def jsavg():
    data = pd.read_sql(
        'daily_agg_2019',
        engine,
        parse_dates=['date'],
        columns=['date', 'jump_score', 'sniff_score']
        )
    if not len(data):
        return "[]"
    data['month_year'] = pd.to_datetime(data['date']).dt.to_period('M')
    data['month_year'] = data['month_year'].dt.strftime('%Y-%m')
    result = data.groupby(['month_year'], as_index=False).mean()
    result.rename(
        columns={
            "month_year": "month", "sniff_score": "sniff_avg", "jump_score": "jump_avg"
        },
        inplace=True)
    return result.to_json(orient='records')


if __name__ == "__main__":
    app.secret_key = 'tN8z8k0Ik6g4fbJ8wWgdSDR7SLLtdAzzy'
    app.run(host='0.0.0.0', port=8099)
