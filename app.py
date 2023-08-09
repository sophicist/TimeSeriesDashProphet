import dash
from dash import dcc,html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import pickle
import plotly.graph_objs as go

# Create a Dash app
app = dash.Dash(__name__)


df = pd.DataFrame()
df['ds'] = pd.date_range(start='2023-01-01', end='2023-12-31')
data = df.copy()

model_filename = "John.pickle"
# Load the pickled model
with open(model_filename, "rb") as file:
    model = pickle.load(file)

# Layout of the app
app.layout = html.Div([
    html.H1("Date Selector and Line Graph"),
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=data['ds'].min(),
        end_date=data['ds'].max(),
        display_format='YYYY-MM-DD',
    ),
    dcc.Graph(id='line-graph'),
])

# Callback to update the line graph based on selected dates
@app.callback(
    Output('line-graph', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)


def update_line_graph(start_date, end_date):
    dz = df[(df['ds'] >= start_date) & (df['ds'] <= end_date)]
    print(dz.head())
    forecast = model.predict(dz)
    trace_forecast = go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Forecasted Values')
    # Create a layout
    layout = go.Layout(title='Prophet Forecasted Values')
    # Create a Plotly figure with the trace and layout
    fig = go.Figure(data=[trace_forecast], layout=layout)
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
