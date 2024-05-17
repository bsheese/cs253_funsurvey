import io
import base64
from flask import Flask, render_template
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from dfprep import prepare_dataframe, get_data, renamelist

local_data = True

if local_data == False:
    # get and prep the dataframe, gets data from url, requires Python SSL certificates setup correctly
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRkK73xD192AdP0jZe6ac9cnVPSeqqbYZmSPnhY2hnY8ANROAOCStRFdvjwFoapv3j2rzMtZ91KXPFm/pub?output=csv"
    df = get_data(url)
else:
    # gets old data from local directory
    df = get_data()

df, label_dict = prepare_dataframe(df, renamelist)



app = Flask(__name__)


@app.context_processor
def inject_vars():
    """
    Makes the label_dict dictionary globally available to all templates.  By using this context processor,
    any template rendered by the application can use label_dict directly without
    needing to have it passed from the view function.
    """
    return {'label_dict': label_dict}


def descriptives_html(df, col_label):
    series = df[col_label]

    # Generate descriptive statistics HTML
    descrip_stats = series.describe()
    descrip_df = pd.DataFrame(descrip_stats).transpose()
    descrip_html = descrip_df.to_html()
    return descrip_html


def valuecount_html(df, col_label):
    series = df[col_label]
    value_counts = series.value_counts(ascending=False)
    value_counts_df = pd.DataFrame(value_counts).head(10)
    value_counts_html = value_counts_df.to_html()
    return value_counts_html


def generate_countplot(df, col_label, horizontal=False):
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


# def text_html(df, col_label):
#     series = df[col_label]
#     series = series.str.strip().str.lower()
#     top_25 = series.value_counts().nlargest(25)
#     barchart = sns.countplot(y=top_25)
#
#     plt.figure(figsize=(10, 8))
#     plt.xlabel('Count')
#     plt.ylabel(col_label.capitalize())
#     plt.title(f'Top 25 Most Common Values in {col_label.capitalize()}')
#
#     # Save the plot to a BytesIO object in memory
#     img = io.BytesIO()
#     plt.savefig(img, format='png')
#     plt.close()
#     img.seek(0)  # Rewind the file
#
#     # Encode the image to base64 string
#     img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
#     return img_base64

def textcount_html(df, col_label):
    # Process the series
    series = df[col_label].str.strip().str.lower().str.title()
    top_25 = series.value_counts().nlargest(25).sort_values(ascending=True)

    # Create the plot
    plt.figure(figsize=(10, 8))
    top_25.plot(kind='barh')
    plt.xlabel('Count')
    plt.ylabel(col_label.capitalize())
    plt.title(f'Top 25 Most Common Values in {col_label.capitalize()}')

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
                           last=df.Timestamp.max(),
                           responses=df.shape[0])


@app.route('/spell')
def spell():
    col_label = 'spell'
    try:
        return render_template('numeric.html',
                               title=col_label,
                               qtext=label_dict[col_label],
                               descrip=descriptives_html(df, col_label),
                               value_counts=valuecount_html(df, col_label),
                               chart='data:image/png;base64,' + generate_countplot(df, col_label))

    except Exception as e:
        return f"An error occurred: {str(e)}"


@app.route('/musicartist')
def musicartist():
    col_label = 'musicartist'
    return render_template('textentry.html',
                           title=col_label,
                           qtext=label_dict[col_label],
                           chart='data:image/png;base64,' + textcount_html(df, col_label))


@app.route('/height')
def height():
    col_label = 'height'
    return render_template('textentry.html',
                           title=col_label,
                           qtext=label_dict[col_label],
                           chart='data:image/png;base64,' + textcount_html(df, col_label))


@app.route('/city')
def city():
    col_label = 'city'
    return render_template('textentry.html',
                           title=col_label,
                           qtext=label_dict[col_label],
                           chart='data:image/png;base64,' + textcount_html(df, col_label))


@app.route('/thirtymin')
def thirtymin():
    col_label = 'thirtymin'
    return render_template('textentry.html',
                           title=col_label,
                           qtext=label_dict[col_label],
                           chart='data:image/png;base64,' + textcount_html(df, col_label))


@app.route('/travel')
def travel():
    col_label = 'travel'
    return render_template('textentry.html',
                           title=col_label,
                           qtext=label_dict[col_label],
                           chart='data:image/png;base64,' + textcount_html(df, col_label))


@app.route('/likepizza')
def likepizza():
    col_label = 'likepizza'
    return render_template('numeric.html',
                           title=col_label,
                           qtext=label_dict[col_label],
                           descrip=descriptives_html(df, col_label),
                           value_counts=valuecount_html(df, col_label),
                           chart='data:image/png;base64,' + generate_countplot(df, col_label))


@app.route('/deepdish')
def deepdish():
    col_label = 'deepdish'
    return render_template('numeric.html',
                           title=col_label,
                           qtext=label_dict[col_label],
                           descrip=descriptives_html(df, col_label),
                           value_counts=valuecount_html(df, col_label),
                           chart='data:image/png;base64,' + generate_countplot(df, col_label))


@app.route('/sport')
def sport():
    col_label = 'sport'
    return render_template('textentry.html',
                           title=col_label,
                           qtext=label_dict[col_label],
                           chart='data:image/png;base64,' + textcount_html(df, col_label))


@app.route('/hangout')
def hangout():
    col_label = 'hangout'
    return render_template('textentry.html',
                           title=col_label,
                           qtext=label_dict[col_label],
                           chart='data:image/png;base64,' + textcount_html(df, col_label))


@app.route('/talk')
def talk():
    col_label = 'talk'
    return render_template('numeric.html',
                           title=col_label,
                           qtext=label_dict[col_label],
                           descrip=descriptives_html(df, col_label),
                           value_counts=valuecount_html(df, col_label),
                           chart='data:image/png;base64,' + generate_countplot(df, col_label))


@app.route('/year')
def year():
    col_label = 'year'
    return render_template('textentry.html',
                           title=col_label,
                           qtext=label_dict[col_label],
                           chart='data:image/png;base64,' + textcount_html(df, col_label))


@app.route('/quote')
def quote():
    col_label = 'quote'
    return render_template('textentry.html',
                           title=col_label,
                           qtext=label_dict[col_label],
                           chart='data:image/png;base64,' + textcount_html(df, col_label))


@app.route('/areacode')
def areacode():
    col_label = 'areacode'
    return render_template('numeric.html',
                           title=col_label,
                           qtext=label_dict[col_label],
                           descrip=descriptives_html(df, col_label),
                           value_counts=valuecount_html(df, col_label),
                           chart='data:image/png;base64,' + generate_countplot(df, col_label))


@app.route('/pets')
def pets():
    col_label = 'pets'
    return render_template('textentry.html',
                           title=col_label,
                           qtext=label_dict[col_label],
                           chart='data:image/png;base64,' + textcount_html(df, col_label))


@app.route('/superpower')
def superpower():
    col_label = 'superpower'
    return render_template('textentry.html',
                           title=col_label,
                           qtext=label_dict[col_label],
                           chart='data:image/png;base64,' + textcount_html(df, col_label))


@app.route('/shoes')
def shoes():
    col_label = 'shoes'
    return render_template('textentry.html',
                           title=col_label,
                           qtext=label_dict[col_label],
                           chart='data:image/png;base64,' + textcount_html(df, col_label))
