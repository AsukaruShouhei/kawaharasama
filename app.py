from flask import Flask, render_template
import scraping as s
import pandas as pd
import numpy as np

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/scraping')
def scraping():
    try:
        if s.getData() == True:
            ress = 'スクレイピングが完了しました。実行後のファイルを確認してください。'
        else:
            ress = 'スクレイピングに失敗しました。'
    except ValueError:
        ress = 'スクレイピングに失敗しました。'
    return render_template('sc.html', ress=ress)


@app.route('/data_includes')
def data_includes():
    df = pd.read_csv("u_data.csv")
    df = df.sort_values(by="date", ascending=True)
    # CSVデータからdateとhiだけを取得
    p = df.loc[:, ['date', 'hi']]
    # 整数に変更
    p['hi'] = np.sign(p['hi'])
    # データの置き換え
    score = []
    for i in p['hi']:
        if i > 0:
            score.append(0)
        else:
            score.append(1)
    p['score'] = pd.DataFrame(score)
    y = p['score']
    p['new'] = y.groupby((y != y.shift()).cumsum()).cumcount() + 1
    data = p[(p['new'] >= 3) & (p['score'] == 1)]
    print(data)
    return render_template('df.html', df=data)


if __name__ == '__main__':
    app.run(debug=True)
