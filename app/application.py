"""
See python notebook on github
"""

from flask import Flask, render_template, session, redirect, url_for, session
import numpy as np
from flask_wtf import FlaskForm
from wtforms import (StringField, RadioField, DecimalField, SubmitField)
from wtforms.validators import DataRequired

import pandas as pd
import numpy as np
import random
import os

from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

clustered_df = pd.read_csv('clustered_df.csv')

init_notebook_mode(connected=True)

def dashboard_make(df_plt, company_name):
    searched_df = df_plt[df_plt['company_name'] == company_name]
    similar_df = df_plt[df_plt['company_name'] != company_name]

    '''
    trace1 = go.Table(
        header=dict(values=[1,2],
                    #fill = dict(color='#C2D4FF'),
                    align = ['left'] * 5),
        cells=dict(values=[1,2],
                   #fill = dict(color='#F5F8FF'),
                   align = ['left'] * 5)
    )
    '''
    trace2 = go.Bar(
        x=[x for x in searched_df['company_name']] + [x for x in similar_df['company_name']],
        y=list(searched_df['total_funding']) + list(similar_df['total_funding']),
        #text=['Text A', 'Text B', 'Text C'],
    )

    trace3 = go.Bar(
        name='Test',
        x=[x for x in searched_df['company_name']] + [x for x in similar_df['company_name']],
        y=list(searched_df['company_max_round']) + list(similar_df['company_max_round']),
        #text=['Text D', 'Text E', 'Text F'],
    )

    trace4 = go.Bar(
        name='Test',
        x=[x for x in searched_df['company_name']] + [x for x in similar_df['company_name']],
        y=list(searched_df['investor_rating']) + list(similar_df['investor_rating']),
        #text=['Text D', 'Text E', 'Text F'],
    )

    fig = tools.make_subplots(rows=2, cols=3,subplot_titles=('Total Funding', 'Rounds','Investor Rating'))

    #fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 1)
    fig.append_trace(trace3, 1, 2)
    fig.append_trace(trace4, 1, 3)


    fig['layout'].update(height=600, width=800,showlegend = False, title=f'Companies Similar To {company_name}')
    #py.iplot(fig, filename='simple-subplot-with-annotations')
    #iplot(fig,filename='basic')

    return fig

def showTopCompanies(df, enteredCompany):

    company_data = df[df["company_name"]==enteredCompany]
    cluster_group = company_data.iloc[0]['final_cluster']
    group = df[df['final_cluster']==cluster_group]
    fig = dashboard_make(group, enteredCompany)
    print("about to print")
    plot(fig, filename='dashboard.html', auto_open=False)
    os.rename("dashboard.html", "templates/dashboard.html")

    html_table = ''.join(group.reset_index(drop=True).to_html().split("\n"))

    return fig, group, html_table

'''End Prediction Stuff '''

application = app = Flask(__name__, static_folder = "static")

app.config['SECRET_KEY'] = 'mysecretkey'

class InfoForm(FlaskForm):
    startup = StringField("Insert Startup Name (or try Random)")
    submit = SubmitField('Submit')

@app.route('/', methods=['GET','POST'])
def index():
    form = InfoForm()

    if form.validate_on_submit():
        # Grab the data from the breed on the form.
        session['Startup'] = form.startup.data;

        if form.startup.data == "Random":
            _, _, html_table = showTopCompanies(clustered_df, random.choice(list(clustered_df["company_name"])))

        else:
            _, _, html_table = showTopCompanies(clustered_df, str(form.startup.data))

        print('Dashboard Created')

        with open('templates/dashboard.html', 'a') as f:
            f.write(' <br><br><br> ')
            f.write(html_table)

        return redirect(url_for("dashboard"))

    return render_template('home.html', form=form)

@app.route('/dashboard')
def dashboard():

    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(debug=True)
