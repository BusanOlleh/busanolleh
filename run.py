from flask import Flask, request, render_template
import pandas as pd
import json

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', pageNum='0')

@app.route('/<num>')
def input1(num):
    if num == 'result': num = '3'
    return render_template('index.html', pageNum=num, zip=zip, enumerate=enumerate)

@app.route('/point', methods=['POST'])
def point():
    data = request.get_json()

    sentiment = data['sentiment']  
    if sentiment == '힐링되는': 
        sentiment = 0
    elif sentiment == '열정적인':  
        sentiment = 1
    elif sentiment == '유익한':  
        sentiment = 2

    tag = data['tag']  # str indexing 

    tags = ['t' + str(i+1) for i, c in enumerate(tag) if c == '1']

    ts = pd.read_csv('travel_spot_data.csv', header=1, index_col=0)

    ts['point'] = 0

    ts.loc[ts['cluster'] == sentiment, 'point'] = 0.5  # 클러스터 점수 합산

    for t in tags:  # 태그 점수 합산
        ts['point'] = ts['point'] + ts[t]

    ts['point'] += ts['rcmded'] * 0.5  # 추천 관광지 점수 합산
   
    # 관광지 행을 random shuffle해서 점수 순 정렬
    ts_top = ts.sample(frac=1).sort_values(['point'], ascending=False)

    # name도 index가 아니라 하나의 column으로 통합
    ts_t = ts_top.reset_index().T
    s = ''
    s += ts_t.loc[:, :4].to_json() # 출력되길 원하는 상위 5개 row값만 넘겨준다.

    return json.dumps(s), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
