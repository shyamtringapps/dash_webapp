import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table as dt
from dash.dependencies import Input, Output
import pandas as pd
from collections import defaultdict

data = pd.read_csv('sample_dump.csv')

df = data[['applicant_id'
    , 'job_openings_id'
    , 'account_id'
    , 'funnel_id'
    , 'position_id'
    , 'derived_preferred_locations', 'job_openings_city'
    , 'derived_applicant_profile_age'
    , 'derived_preferred_industries', 'job_openings_industry', 'job_openings_title'
    , 'derived_dist_btwn_candidate_and_job'
    , 'similarity_score_actual']]

app = dash.Dash(__name__)

all_options = defaultdict(list)
for k, v in zip(df.job_openings_city.values, df.job_openings_title.values):
    all_options[k].append(v)

app.layout = html.Div(
    children=[
        html.H1('Dashboard'),
        html.H4('Select city'),
        dcc.Dropdown(
            id='city',
            options=[{'label': st, 'value': st} for st in all_options.keys()],
            placeholder="Select City",
            style=dict(
                width='40%',
                verticalAlign="middle"
            )
        ),
        html.H4('Select title'),
        dcc.Dropdown(
            id='title',
            placeholder="Select title",
            style=dict(
                width='40%',
                verticalAlign="middle"
            )
        ),
        html.H4('Select preferred circle(km)'),
        dcc.Slider(
            id='km',
            min=0,
            max=20,
            step=0.5,
            value=0,
            marks={
                0: {'label': '0 km', 'style': {'color': '#77b0b1'}},
                5: {'label': '5 km'},
                10: {'label': '10 km'},
                15: {'label': '15km'},
                20: {'label': '20 km', 'style': {'color': '#f50'}}
            },
            updatemode='drag',
        ),
        html.Div(id='slider-output-container'),
        html.Hr(),
        html.H4('Data filtered'),
        dt.DataTable(id='table-container', columns=[{'id': c, 'name': c} for c in df.columns.values])])


@app.callback(
    Output('title', 'options'),
    [Input('city', 'value')])
def set_cities_options(selected_country):
    return [{'label': i, 'value': i} for i in all_options[selected_country]]


@app.callback(
    Output('table-container', 'data'),
    [Input('title', 'value'), Input('km', 'value')])
def display_table(title, km):
    dff = (df[df['job_openings_title'] == title])
    dff = dff[dff['derived_dist_btwn_candidate_and_job'] <= km]
    return dff.to_dict('records')


@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    [dash.dependencies.Input('km', 'value')])
def update_output(value):
    return 'You have selected {}'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)
