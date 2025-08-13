from flask import Flask, render_template, url_for, redirect
import pandas as pd
import matplotlib.pyplot as plt
import os

clas = Flask(__name__)
data_df = pd.DataFrame()

@clas.route('/')
def home():
    return render_template('homepage.html')

@clas.route('/next')
def next():
    global data_df
    data_df = pd.read_csv('StressLevelDataset.csv')
    data_df = data_df[["anxiety_level", "depression"]]
    return render_template('next.html', table = data_df.head().to_html(index = False))

@clas.route('/bar')
def bar_chart():
    if data_df.empty:
        return redirect('/next')

    plt.figure(figsize=(10,6))
    plt.bar(data_df["anxiety_level"], data_df["depression"])
    plt.xlabel("anxiety level")
    plt.ylabel("depression")
    chart_url = os.path.join('static', 'chart.png')
    plt.savefig(chart_url)
    plt.close()

    return render_template("barchart.html", bar_graph = url_for('static', filename =  'chart.png'))

@clas.route('/pie')
def pie_chart():
    if data_df.empty:
        return redirect('/next')
    
    plt.figure(figsize=(8,6))
    data = data_df["anxiety_level"].head().value_counts()
    plt.pie(data.values, labels=data.index)
    chart_url = os.path.join('static', 'chart.png')
    plt.savefig(chart_url)
    plt.close()

    return render_template('piechart.html', pie_chart = url_for('static', filename = "chart.png"))

if __name__ == "__main__":

    clas.run(port=3000, host = "0.0.0.0", debug = False)
