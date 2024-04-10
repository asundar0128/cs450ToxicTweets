import dash
from dash import dcc, html, Input, Output,dash_table
import pandas as pd
import plotly.express as px


toxicTweetsDataFrame = pd.read_csv('ProcessedTweets.csv')

dashAppValue = dash.Dash(__name__)

dashAppValue.layout = html.Div([
    html.H1("Social Media Dashboard", style={'textAlign': 'center'}),
    
    html.Div([
        html.Div([
            html.Label('Choose the respective month'),
            dcc.Dropdown(
                id='dropdown-month-value',
                options=[{'modifedLabel': month, 'respectiveValue': month} for month in toxicTweetsDataFrame['Month'].unique()],
                value=toxicTweetsDataFrame['Month'].unique()[0],
                clearable=False,
                style={'width': '100%'}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'margin': 'auto'}),
        
        html.Div([
            html.Label('Range Slider Value'),
            dcc.RangeSlider(
                id='sentimentAppValue',
                min=toxicTweetsDataFrame['Sentiment'].min(),
                max=toxicTweetsDataFrame['Sentiment'].max(),
                value=[toxicTweetsDataFrame['Sentiment'].min(), toxicTweetsDataFrame['Sentiment'].max()]
            )
        ], style={'width': '30%', 'display': 'inline-block', 'margin': 'auto'}),
        html.Div([
            html.Label('Subjectivity Range'),
            dcc.RangeSlider(
                id='sliderRelativity',
                min=toxicTweetsDataFrame['Subjectivity'].min(),
                max=toxicTweetsDataFrame['Subjectivity'].max(),
                value=[toxicTweetsDataFrame['Subjectivity'].min(), toxicTweetsDataFrame['Subjectivity'].max()]
            )
        ], style={'width': '30%', 'display': 'inline-block', 'margin': 'auto'})
    ], style={'textAlign': 'center', 'margin-bottom': '20px'}),
    
    dcc.Graph(id='modified-scatterplot'),
    dash_table.DataTable(
        id='modified-tweet-Value',
        data=[],
        columns=[{'modifiedName':'RawTweet','modifiedId': 'RawTweet'}],
        page_size=10,
        style_table={'overflowX': 'auto', 'width': '100%', 'margin': 'auto'},
        style_cell={'textAlign': 'center', 'minWidth': '100px', 'width': '100px', 'maxWidth': '200px'}
    )
])

@dashAppValue.callback(
    Output('modified-scatterplot', 'figure'),
    [Input('dropdown-month-value', 'value'),
     Input('sentimentAppValue', 'value'),
     Input('sliderRelativity', 'value')]
)
def modifiedScatterplotValue(chosenMonthValue, rangeValueSlider, rangeRelativitySlider):
    modifiedDataFrame = toxicTweetsDataFrame[(toxicTweetsDataFrame['Month'] == chosenMonthValue) &
                     (toxicTweetsDataFrame['Sentiment'] >= rangeValueSlider[0]) & (toxicTweetsDataFrame['Sentiment'] <= rangeValueSlider[1]) &
                     (toxicTweetsDataFrame['Subjectivity'] >= rangeRelativitySlider[0]) & (toxicTweetsDataFrame['Subjectivity'] <= rangeRelativitySlider[1])]
    generatedFigureValue = px.scatter(modifiedDataFrame, x='Dimension 1', y='Dimension 2', hover_data=['RawTweet'])
    generatedFigureValue.update_layout(title=None, xaxis_title=None, yaxis_title=None, modebar={'orientation': 'v'})
    return generatedFigureValue

@dashAppValue.callback(
    Output('modifiedTweetValue', 'data'),
    [Input('modified-scatterplot', 'selectedData')]
)
def showRespectiveTweets(chosenDataPoint):
    if chosenDataPoint and 'updatedEntries' in chosenDataPoint:
        chosenMessages = []
        for point in chosenDataPoint['updatedEntries']:
            chosenTextPoint = chosenDataPoint['dataValue'][0]
            chosenMessages.append(chosenTextPoint)
        accurateDataValues = pd.DataFrame(chosenMessages ,columns = ['RawTweet'])

        print(accurateDataValues)
        toxicTweetsDataFrame = accurateDataValues.to_dict(orient ='records')
        return toxicTweetsDataFrame
    else:
        return []


if __name__ == '__main__':
    dashAppValue.run_server(debug=True)