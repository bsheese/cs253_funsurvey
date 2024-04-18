
import io
import base64
import os
from flask import Flask, request, g, redirect, url_for, render_template, flash, send_file
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

app = Flask(__name__)



# survey data url
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRkK73xD192AdP0jZe6ac9cnVPSeqqbYZmSPnhY2hnY8ANROAOCStRFdvjwFoapv3j2rzMtZ91KXPFm/pub?output=csv"

renamelist = ['Timestamp', 'musicartist', 'height', 'city', 'thirtymin', 'travel', \
              'likepizza', 'deepdish', 'sport', 'spell', 'hangout', 'talk', \
              'year', 'quote', 'areacode', 'pets', 'superpower', 'shoes']

# create data frame from url
df = pd.read_csv(url)

# assign original headers to list
survey_questions = df.columns.to_list()

# replace with column names easier to work with
df.columns = renamelist

# drop duplicates
df = df.drop_duplicates(subset=df.columns[1:])
df.Timestamp = pd.to_datetime(df.Timestamp)

label_dict = {}
for i in range(len(renamelist)):
    label_dict[renamelist[i]] = survey_questions[i]

@app.context_processor
def inject_vars():
    return {'label_dict': label_dict}


def descriptives_html(col_label):
    series = df[col_label]

    # Generate descriptive statistics HTML
    descrip_stats = series.describe()
    descrip_df = pd.DataFrame(descrip_stats).transpose()
    descrip_html = descrip_df.to_html()
    return descrip_html

def valuecount_html(col_label):
    series = df[col_label]
    value_counts = series.value_counts(ascending=False)
    value_counts_df = pd.DataFrame(value_counts).head(10)
    value_counts_html = value_counts_df.to_html()
    return value_counts_html



def generate_countplot(col_label, horizontal=False):
    series = df[col_label]

    if horizontal:
        barchart = sns.countplot(y=series)
    else:
        barchart = sns.countplot(x=series)

    # Save the plot to a BytesIO object in memory
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)  # Rewind the file

    # Encode the image to base64 string
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    return img_base64


@app.route('/')
def home():
    df_descriptives = df.describe().to_html()
    return render_template('index.html',
                           label_dict=label_dict,
                           first=df.Timestamp.min(),
                           last =df.Timestamp.max(),
                           responses=df.shape[0])

@app.route('/spell')
def spell():
    col_label = 'spell'
    return render_template('numeric.html',
                           title=col_label,
                           qtext=label_dict[col_label],
                           descrip=descriptives_html(col_label),
                           value_counts=valuecount_html(col_label),
                           chart='data:image/png;base64,' + generate_countplot(col_label))

@app.route('/musicartist')
def musicartist():
    col_label = 'musicartist'
    return render_template('numeric.html',
                           title=col_label,
                           qtext=label_dict[col_label],
                           descrip=descriptives_html(col_label),
                           value_counts=valuecount_html(col_label),
                           chart='data:image/png;base64,' + generate_countplot(col_label))

@app.route('/height')
def height():
    return render_count('height', horizontal=True)
@app.route('/city')
def city():
    return render_count('city', horizontal=True)
@app.route('/thirtymin')
def thirtymin():
    return render_count('thirtymin', horizontal=True)
@app.route('/travel')
def travel():
    return render_count('travel', horizontal=True)

@app.route('/likepizza')
def likepizza():
    return render_count('likepizza', horizontal=False)

@app.route('/deepdish')
def deepdish():
    return render_count('deepdish', horizontal=True)

@app.route('/sport')
def sport():
    return render_count('sport', horizontal=True)
@app.route('/hangout')
def hangout():
    return render_count('hangout', horizontal=True)

@app.route('/talk')
def talk():
    return render_count('talk', horizontal=True)
@app.route('/year')
def year():
    return render_count('year', horizontal=True)

@app.route('/quote')
def quote():
    return render_count('quote', horizontal=True)
@app.route('/areacode')
def areacode():
    return render_count('areacode', horizontal=True)
@app.route('/pets')
def pets():
    return render_count('pets', horizontal=True)
@app.route('/superpower')
def superpower():
    return render_count('superpower', horizontal=True)
@app.route('/shoes')
def shoes():
    return render_count('shoes', horizontal=True)

