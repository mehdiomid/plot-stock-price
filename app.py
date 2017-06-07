from flask import Flask, render_template, request
from datetime import datetime
import requests
import json
import pandas as pd
import numpy as np
import bokeh.charts as bc
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from bokeh.models import ColumnDataSource


app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def homepage():
    if request.method == 'GET':
        return render_template('myProject.html')
    else:
        #request was a POST
        app.vars['name'] = request.form['ticker']
        app.symbol=request.form['ticker']
        app.vars['action'] = request.form['features']
        return render_template('userinfo',ticker=app.vars['name'])

        

#lab=app.symbol       
@app.route('/graph',methods=['GET','POST'])
def userinfo():
 #lab=request.form['ticker']
 APIKEY='eEN8AH1r1CE7sRFeJ33Z'
 ticker=request.form['ticker']
 if ticker == '':
     return render_template('noinput.html')
 else:
     url='https://www.quandl.com/api/v3/datasets/WIKI/'+ticker+'/data.json?api_key='+APIKEY
     res=requests.get(url)
     d=res.json()
     col_names=d['dataset_data']['column_names']
     df=pd.DataFrame(d['dataset_data']['data'],columns=col_names)
     df['Date'] = pd.to_datetime(df['Date'])
     source=ColumnDataSource(data=df)
     pf=figure(x_axis_type='datetime',x_axis_label='Date',y_axis_label='US Dollars', title='stock price')
     features=request.form['features']
     pf.line('Date', features, source=source)
     script, div = components(pf)
     # grab the static resources
     js_resources = INLINE.render_js()
     css_resources = INLINE.render_css()
     # render template
     html = render_template(
           'graphic.html',
           features=features,
           ticker=ticker,
           plot_script=script,
           plot_div=div,
           js_resources=js_resources,
           css_resources=css_resources,
     )
     return encode_utf8(html)

@app.errorhandler(500)
def page_not_found(e):
    return render_template('QuandleError.html')
     
     
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
#    app.run(debug=True, use_reloader=True)

