# Import required libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import numpy as np
import os

# Initialize the app with custom styling
app = dash.Dash(
    __name__, 
    external_stylesheets=[
        dbc.themes.FLATLY,
        'https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap'
    ]
)

# This is important for Render deployment
server = app.server

# Custom CSS for consistent font styling
app.index_string = '''<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            * {
                font-family: 'Bebas Neue', sans-serif;
            }
            .regular-text {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            }
            .card-body p, .card-body text {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            }
            .card {
                margin-bottom: 1rem;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>'''

# Create DataFrames with the updated data
monthly_data = pd.DataFrame({
    'Metric': ['Total Transactions', 'Transaction Volume (KES)', 'Successful Transactions', 
               'Failed Transactions', 'Success Rate (%)', 'Unique Remitters', 
               'Unique Recipients', 'Unique Countries'],
    'Annual Total': [38091, 2172008165.44, 34292, 2804.84, 87, 16275, 18225, 16],
    'Monthly Average': [3174.25, 181000680.45, 2857.67, 233.74, 87, 1356.25, 1518.75, 6.33],
    'Maximum': [8217, 523575404.54, 7136, 829, 97.6, 3367, 3858, 16],
    'Minimum': [31, 925.00, 12, 1, 38.7, 3, 6, 2]
})

failure_data = pd.DataFrame({
    'Reason': ['Insufficient Balance', 'Other', 'System Error', 'Invalid Account', 
               'Invalid Credit Party', 'Timed Out', 'General Failure', 'SOAP Error', 'Limit Exceeded'],
    'Count': [2216, 592, 437, 251, 83, 133, 23, 6, 2],
    'Percentage': [58.3, 15.6, 11.5, 6.6, 2.2, 3.5, 0.6, 0.2, 0.1]
})

country_data = pd.DataFrame({
    'Country': ['United Kingdom (GBR)', 'United States (USA)', 'Canada (CAN)', 
                'Kenya (KEN)', 'Nigeria (NGA)', 'Tanzania (TZA)', 'Others'],
    'Volume_KES': [961197746.35, 422501849.21, 68916278.01, 
                   32036111.63, 6352832.02, 391069.01, 211543.12],
    'Transactions': [18050, 7906, 1842, 1339, 395, 6, 18]
})

client_data = pd.DataFrame({
    'Client': ['Lemfi', 'DLocal', 'Tangent', 'Nala', 'Wapipay', 'Brij', 
              'Cellulant', 'Others'],
    'Volume': [1701947843.25, 410741870.10, 31148619.48, 13119614.16, 
              15022090.45, 28085.00, 43.00, 0.00],
    'Transactions': [29281, 4547, 203, 173, 42, 42, 4, 0],
    'Market_Share': [78.36, 18.91, 1.43, 0.60, 0.69, 0.01, 0.00, 0.00]
})

recipients_data = pd.DataFrame({
    'Bank': ['ABSA Bank', 'Cooperative Bank', 'DT Bank', 'Equity Bank', 
            'Family Bank', 'I&M Bank', 'KCB Bank', 'NCBA Bank'],
    'Volume': [7282025.65, 11802956.97, 7677251.81, 24819864.19,
              9481656.86, 9501100.76, 17038871.74, 11536537.68],
    'Transactions': [139, 338, 124, 889, 215, 244, 348, 195],
    'Market_Share': [6.53, 10.58, 6.88, 22.25, 8.50, 8.52, 15.27, 10.34]
})

private_individual_data = pd.DataFrame({
    'Month': ['January', 'February', 'March'],
    'Volume': [956150.00, 1762875.00, 3089338.00],
    'Transactions': [6, 6, 13]
})

hourly_data = pd.DataFrame({
    'Hour': [f'{i:02d}:00' for i in range(24)],
    'Volume': [
        27533935.96, 28073270.30, 29035102.50, 24136418.10, 20726459.19,
        18337660.33, 31046599.22, 18624343.36, 17163342.76, 17538441.06,
        15470631.39, 18356204.26, 18473250.50, 16966374.97, 21376240.02,
        24886442.52, 26430533.46, 36983605.96, 32593463.80, 33624440.10,
        35671112.12, 41021127.01, 41365601.43, 47980870.44
    ]
})

# App Layout
app.layout = dbc.Container([
    # Header with logo and title
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(src='/assets/vngrd.PNG',
                     className='logo', 
                     style={'height': '150px', 'object-fit': 'contain'})
            ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'padding': '40px', 'marginBottom': '30px', 'width': '100%'}),
            html.H1("2024 Annual Business Transfer Analysis", 
                   className="text-primary text-center mb-4",
                   style={'letterSpacing': '2px'})
        ])
    ]),

    # Key Metrics Cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Total Annual Transactions", className="card-title text-center"),
                    html.H2(f"{monthly_data.loc[0, 'Annual Total']:,.0f}", 
                           className="text-primary text-center"),
                    html.P([
                        html.Span("Monthly Average: ", className="regular-text"),
                        html.Span(f"{monthly_data.loc[0, 'Monthly Average']:,.0f}",
                                className="regular-text text-success")
                    ], className="text-center")
                ])
            ], className="shadow-sm")
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Average Success Rate", className="card-title text-center"),
                    html.H2([
                        f"{monthly_data.loc[4, 'Annual Total']}",
                        html.Small("%", className="text-muted")
                    ], className="text-primary text-center"),
                    html.P([
                        html.Span("Peak: ", className="regular-text"),
                        html.Span(f"{monthly_data.loc[4, 'Maximum']}%",
                                className="regular-text text-success")
                    ], className="text-center")
                ])
            ], className="shadow-sm")
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Total Volume (KES)", className="card-title text-center"),
                    html.H2(f"{monthly_data.loc[1, 'Annual Total']/1e9:.2f}B", 
                           className="text-primary text-center"),
                    html.P([
                        html.Span("Monthly Average: ", className="regular-text"),
                        html.Span(f"KES {monthly_data.loc[1, 'Monthly Average']/1e6:.1f}M",
                                className="regular-text text-success")
                    ], className="text-center")
                ])
            ], className="shadow-sm")
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Total Unique Remitters", className="card-title text-center"),
                    html.H2(f"{monthly_data.loc[5, 'Annual Total']:,.0f}", 
                           className="text-primary text-center"),
                    html.P([
                        html.Span("Monthly Average: ", className="regular-text"),
                        html.Span(f"{monthly_data.loc[5, 'Monthly Average']:,.0f}",
                                className="regular-text text-success")
                    ], className="text-center")
                ])
            ], className="shadow-sm")
        ])
    ], className="mb-4"),

    # Geographic Distribution
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Geographic Distribution"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=go.Figure(data=[
                            go.Bar(
                                name='Volume (KES)',
                                x=country_data['Country'],
                                y=country_data['Volume_KES'],
                                yaxis='y',
                                marker_color='rgba(26, 118, 255, 0.8)'
                            ),
                            go.Scatter(
                                name='Transactions',
                                x=country_data['Country'],
                                y=country_data['Transactions'],
                                yaxis='y2',
                                mode='lines+markers',
                                marker_color='rgba(255, 128, 0, 0.8)'
                            )
                        ]).update_layout(
                            yaxis=dict(title='Volume (KES)', type='log', side='left'),
                            yaxis2=dict(title='Transactions', type='log', side='right', overlaying='y'),
                            xaxis_tickangle=-45,
                            height=500,
                            legend=dict(orientation="h", yanchor="bottom", y=1.02),
                            margin=dict(l=50, r=50, t=30, b=100)
                        )
                    )
                ])
            ], className="shadow-sm")
        ])
    ], className="mb-4"),
    
    # Failure Analysis and Client Market Share
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Annual Failure Analysis"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=px.treemap(
                            failure_data,
                            path=['Reason'],
                            values='Count',
                            color='Percentage',
                            hover_data=['Percentage'],
                            color_continuous_scale='RdYlBu_r'
                        ).update_layout(
                            height=400,
                            margin=dict(l=20, r=20, t=30, b=20)
                        )
                    )
                ])
            ], className="shadow-sm")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Client Market Share"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=px.pie(
                            client_data,
                            values='Volume',
                            names='Client',
                            title='Transaction Volume by Client',
                            hover_data=['Transactions', 'Market_Share']
                        ).update_layout(
                            height=400
                        )
                    ),
                    html.Div([
                        html.Div([
                            html.Img(
                                src=f'/assets/{client.lower()}.png',
                                style={
                                    'width': '60px',
                                    'height': '60px',
                                    'objectFit': 'contain',
                                    'margin': '5px'
                                }
                            ) for client in client_data['Client']
                        ], style={
                            'display': 'flex',
                            'flexWrap': 'wrap',
                            'justifyContent': 'center',
                            'alignItems': 'center',
                            'marginTop': '20px'
                        })
                    ])
                ])
            ], className="shadow-sm")
        ], width=6)
    ], className="mb-4"),

# Bank Recipients Analysis
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Bank Recipients Overview"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=go.Figure(data=[
                            go.Bar(
                                name='Transaction Volume',
                                x=recipients_data['Bank'],
                                y=recipients_data['Volume'],
                                marker_color='rgba(26, 118, 255, 0.8)',
                                yaxis='y'
                            ),
                            go.Scatter(
                                name='Market Share (%)',
                                x=recipients_data['Bank'],
                                y=recipients_data['Market_Share'],
                                mode='lines+markers',
                                marker_color='rgb(255, 128, 0)',
                                yaxis='y2'
                            )
                        ]).update_layout(
                            title='Bank Recipients - Volume vs Market Share',
                            yaxis=dict(
                                title='Volume (KES)',
                                titlefont=dict(color='rgba(26, 118, 255, 0.8)'),
                                tickfont=dict(color='rgba(26, 118, 255, 0.8)')
                            ),
                            yaxis2=dict(
                                title='Market Share (%)',
                                titlefont=dict(color='rgb(255, 128, 0)'),
                                tickfont=dict(color='rgb(255, 128, 0)'),
                                overlaying='y',
                                side='right'
                            ),
                            xaxis_tickangle=-45,
                            height=500,
                            margin=dict(l=50, r=50, t=50, b=100),
                            legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=1
                            )
                        )
                    )
                ])
            ], className="shadow-sm")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Transaction Distribution by Bank"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=px.pie(
                            recipients_data,
                            values='Transactions',
                            names='Bank',
                            title='Transaction Count Distribution',
                            hover_data=['Volume', 'Market_Share']
                        ).update_layout(
                            height=500,
                            margin=dict(l=20, r=20, t=50, b=50)
                        )
                    )
                ])
            ], className="shadow-sm")
        ], width=6)
    ], className="mb-4"),

    # Transaction Volume and Private Individual Analysis
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Bank Transaction Metrics"),
                dbc.CardBody([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.H4("Key Statistics", className="text-center mb-4"),
                                html.Div([
                                    html.P([
                                        "Highest Volume Bank: ",
                                        html.Span("Equity Bank", className="font-weight-bold"),
                                        f" (KES {24819864.19:,.2f})"
                                    ], className="mb-2"),
                                    html.P([
                                        "Most Transactions: ",
                                        html.Span("889", className="font-weight-bold"),
                                        " (Equity Bank)"
                                    ], className="mb-2"),
                                    html.P([
                                        "Average Transaction Value: ",
                                        html.Span(f"KES {recipients_data['Volume'].sum() / recipients_data['Transactions'].sum():,.2f}", 
                                                className="font-weight-bold")
                                    ], className="mb-2"),
                                    html.Hr(),
                                    html.H5("Private Individual Transactions", className="mt-3 mb-3"),
                                    html.P([
                                        "Total Volume: ",
                                        html.Span(f"KES {private_individual_data['Volume'].sum():,.2f}",
                                                className="font-weight-bold")
                                    ], className="mb-2"),
                                    html.P([
                                        "Total Transactions: ",
                                        html.Span(str(private_individual_data['Transactions'].sum()),
                                                className="font-weight-bold")
                                    ], className="mb-2")
                                ], className="p-3 border rounded")
                            ])
                        ])
                    ])
                ])
            ], className="shadow-sm")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Private Individual Transactions Trend"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=go.Figure(data=[
                            go.Bar(
                                name='Volume',
                                x=private_individual_data['Month'],
                                y=private_individual_data['Volume'],
                                marker_color='rgba(26, 118, 255, 0.8)'
                            ),
                            go.Scatter(
                                name='Transactions',
                                x=private_individual_data['Month'],
                                y=private_individual_data['Transactions'],
                                mode='lines+markers',
                                marker_color='rgb(255, 128, 0)',
                                yaxis='y2'
                            )
                        ]).update_layout(
                            title='Private Individual Transaction Trends',
                            yaxis=dict(title='Volume (KES)'),
                            yaxis2=dict(
                                title='Number of Transactions',
                                overlaying='y',
                                side='right'
                            ),
                            height=500,
                            margin=dict(l=50, r=50, t=50, b=50),
                            legend=dict(orientation="h", y=1.1)
                        )
                    )
                ])
            ], className="shadow-sm")
        ], width=6)
    ], className="mb-4")

], fluid=True, className="p-4")

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run_server(debug=False, host='0.0.0.0', port=port)
