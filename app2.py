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

# Add the logo mappings here, before app initialization
# File name mappings for clients
CLIENT_LOGOS = {
    'Lemfi': 'CLIENT_LOGOS/LEMFI.png',
    'DLocal': 'CLIENT_LOGOS/DLocal.png',
    'Tangent': 'CLIENT_LOGOS/Tangent.jpg',
    'Nala': 'CLIENT_LOGOS/Nala.png',
    'Wapipay': 'CLIENT_LOGOS/wapipay.jpg',
    'Cellulant': 'CLIENT_LOGOS/Cellulant.png',
    'Hello FXBud': 'CLIENT_LOGOS/fxbud.jpg',
    'Finpesa': 'CLIENT_LOGOS/finpesa.png'
}

# Initialize the app
app = dash.Dash(
    __name__, 
    external_stylesheets=[
        dbc.themes.FLATLY,
        'https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap'
    ]
)

# This is important for Render deployment
server = app.server

# Custom CSS
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

# Monthly data
monthly_data = pd.DataFrame({
    'Month': ['January', 'February', 'March', 'April', 'May', 'June', 
             'July', 'August', 'September', 'October', 'November', 'December'],
    'Transactions': [133641, 171044, 200841, 204680, 197654, 189258, 
                    182504, 183429, 84383, 169780, 138824, 68452],
    'Volume': [2013687811.26, 2490772705.46, 2776712059.66, 2771003331.42, 2732297727.71, 
               2539282672.75, 2551967296.20, 2890018921.76, 1411203322.06, 2230387153.64, 
               1849984455.07, 987131225.49],
    'Success_Rate': [95.47, 97.72, 96.65, 97.87, 99.05, 98.17, 
                    95.36, 95.11, 94.85, 98.13, 94.52, 94.03],
    'Unique_Remitters': [20610, 20219, 17487, 26118, 16178, 23345, 
                        28163, 28799, 23795, 34715, 25236, 18104],
    'Unique_Recipients': [34553, 50852, 75630, 85424, 66600, 73019, 
                         67567, 71636, 42967, 80602, 63104, 38295]
})

# Failure data
failure_data = pd.DataFrame({
    'Reason': ['General Failure', 'Limit Exceeded', 'Invalid Credit Party', 
               'Insufficient Balance', 'SOAP Error', 'Timed Out', 'System Error',
               'Connectivity Error', 'Invalid Account', 'Invalid Details', 'Other'],
    'Total': [833, 11376, 5416, 31173, 1248, 1640, 485, 194, 557, 4695, 2312],
    'Percentage': [1.39, 18.98, 9.04, 52.02, 2.08, 2.74, 0.81, 0.32, 0.93, 7.83, 3.86]
})

# Updated hourly data with half-hour intervals
hourly_data = pd.DataFrame({
    'Hour': ['12:00:00 AM', '12:30:00 AM', '1:00:00 AM', '1:30:00 AM', '2:00:00 AM', '2:30:00 AM', 
            '3:00:00 AM', '3:30:00 AM', '4:00:00 AM', '4:30:00 AM', '5:00:00 AM', '5:30:00 AM', 
            '6:00:00 AM', '6:30:00 AM', '7:00:00 AM', '7:30:00 AM', '8:00:00 AM', '8:30:00 AM', 
            '9:00:00 AM', '9:30:00 AM', '10:00:00 AM', '10:30:00 AM', '11:00:00 AM', '11:30:00 AM',
            '12:00:00 PM', '12:30:00 PM', '1:00:00 PM', '1:30:00 PM', '2:00:00 PM', '2:30:00 PM',
            '3:00:00 PM', '3:30:00 PM', '4:00:00 PM', '4:30:00 PM', '5:00:00 PM', '5:30:00 PM',
            '6:00:00 PM', '6:30:00 PM', '7:00:00 PM', '7:30:00 PM', '8:00:00 PM', '8:30:00 PM',
            '9:00:00 PM', '9:30:00 PM', '10:00:00 PM', '10:30:00 PM', '11:00:00 PM', '11:30:00 PM'],
    'Volume': [239901818.81, 244991276.09, 225345783.38, 239690642.99, 261409055.99, 286688826.43,
              336935592.92, 365831601.29, 426891279.31, 475891128.44, 518967965.34, 558806726.45,
              593022936.74, 611179510.15, 685317245.20, 667263464.74, 692677269.65, 697109566.67,
              739877303.90, 735930672.71, 744234540.79, 759891766.66, 784129511.47, 760450859.64,
              796315758.28, 783213808.44, 834070722.89, 841420254.91, 802473919.21, 800976384.25,
              785374503.63, 766217167.73, 762218552.20, 721923234.09, 658575263.68, 643863311.42,
              611843138.71, 611227839.98, 585600775.32, 533709014.43, 509964810.15, 461427440.03,
              444715572.40, 400121854.04, 355988522.99, 336914663.10, 293197740.74, 250658084.10],
    'Count': [13227, 12799, 12627, 13473, 15001, 16630, 19864, 22101, 26156, 29393, 32579, 35504,
              38688, 40719, 44114, 43998, 46626, 47937, 50107, 50920, 53048, 51906, 54098, 54047,
              56413, 66726, 69391, 60756, 60297, 60479, 59526, 58740, 56640, 53619, 50586, 48568,
              45561, 44122, 40435, 37372, 33066, 29971, 27130, 24256, 21395, 19049, 16791, 14891]
})

# Country data - excluding Unknown
country_data = pd.DataFrame({
    'Country': ['CAN', 'FIN', 'GBR', 'GER', 'IRL', 'KEN', 'NGA', 'UGA', 'USA', 'Unknown'],
    'Volume': [1517951948.64, 307421630.62, 11315946583.70, 101630751.00, 153890861.47,
               846415656.43, 101777855.36, 896761980.11, 6791147045.70, 4772819388.13],
    'Transactions': [118717, 28193, 864380, 6034, 10630, 68183, 9028, 1609, 402476, 327200],
    'Market_Share': [5.66, 1.15, 42.21, 0.38, 0.57, 3.16, 0.38, 3.35, 25.33, 17.81]
})

# Daily data from the PDF
daily_data = pd.DataFrame({
    'Day': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
    'Volume': [3446887082.69, 3542203701.92, 3856600588.57, 4174561072.82, 
               5582156391.24, 3962547257.90, 2679492587.34],
    'Count': [231857, 236668, 249814, 264715, 348966, 297996, 231426]
})

# Client data
client_data = pd.DataFrame({
    'Client': ['Lemfi', 'Cellulant', 'Nala', 'DLocal', 'Wapipay', 'Hello FXBud', 
              'Finpesa', 'Tangent', 'Others'],
    'Volume': [11606556833.85, 6280089643.65, 8055904624.99, 248808932.68, 
               1510015.74, 617699.08, 973692826.00, 76931592.49, 0.00],
    'Transactions': [836080, 443517, 560706, 16028, 174, 103, 1571, 3090, 0],
    'Market_Share': [42.60, 23.05, 29.57, 0.91, 0.01, 0.00, 3.57, 0.28, 0.00]
})

# Start App Layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(
                    src='assets/vngrd.PNG',
                    className='logo', 
                    style={'height': '150px', 'object-fit': 'contain'}
                )
            ], style={
                'display': 'flex', 
                'justifyContent': 'center', 
                'alignItems': 'center', 
                'padding': '40px', 
                'marginBottom': '30px', 
                'width': '100%'
            }),
            html.H1(
                "2024 Mobile Wallet Transfer Analysis", 
                className="text-primary text-center mb-4",
                style={'letterSpacing': '2px'}
            )
        ])
    ]),

    # Key Metrics Cards
    dbc.Row([
        # Total Transactions Card
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Total Annual Transactions", className="card-title text-center"),
                    html.H2(
                        f"{monthly_data['Transactions'].sum():,.0f}", 
                        className="text-primary text-center"
                    ),
                    html.P([
                        html.Span("Monthly Average: ", className="regular-text"),
                        html.Span(
                            f"{monthly_data['Transactions'].mean():,.0f}",
                            className="regular-text text-success"
                        )
                    ], className="text-center")
                ])
            ], className="shadow-sm")
        ]),
        
        # Success Rate Card
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Average Success Rate", className="card-title text-center"),
                    html.H2([
                        f"{monthly_data['Success_Rate'].mean():.1f}",
                        html.Small("%", className="text-muted")
                    ], className="text-primary text-center"),
                    html.P([
                        html.Span("Peak: ", className="regular-text"),
                        html.Span(
                            f"{monthly_data['Success_Rate'].max():.1f}%",
                            className="regular-text text-success"
                        )
                    ], className="text-center")
                ])
            ], className="shadow-sm")
        ]),
        
        # Total Volume Card
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Total Volume (KES)", className="card-title text-center"),
                    html.H2(
                        f"{monthly_data['Volume'].sum()/1e9:.2f}B", 
                        className="text-primary text-center"
                    ),
                    html.P([
                        html.Span("Monthly Average: ", className="regular-text"),
                        html.Span(
                            f"KES 2.27B",
                            className="regular-text text-success"
                        )
                    ], className="text-center")
                ])
            ], className="shadow-sm")
        ]),

        # Unique Users Card
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Total Unique Remitters", className="card-title text-center"),
                    html.H2(
                        f"{monthly_data['Unique_Remitters'].sum():,.0f}", 
                        className="text-primary text-center"
                    ),
                    html.P([
                        html.Span("Monthly Average: ", className="regular-text"),
                        html.Span(
                            f"{monthly_data['Unique_Remitters'].mean():,.0f}",
                            className="regular-text text-success"
                        )
                    ], className="text-center")
                ])
            ], className="shadow-sm")
        ])
    ], className="mb-4"),

# Monthly Volume Trends
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Monthly Transaction Analysis"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=go.Figure(data=[
                            go.Bar(
                                name='Volume',
                                x=monthly_data['Month'],
                                y=monthly_data['Volume']/1e6,
                                marker_color='rgba(26, 118, 255, 0.8)',
                                yaxis='y'
                            ),
                            go.Scatter(
                                name='Success Rate',
                                x=monthly_data['Month'],
                                y=monthly_data['Success_Rate'],
                                mode='lines+markers',
                                marker=dict(
                                    size=8,
                                    color='rgba(255, 128, 0, 0.8)'
                                ),
                                line=dict(
                                    width=2,
                                    color='rgba(255, 128, 0, 0.8)'
                                ),
                                yaxis='y2'
                            )
                        ]).update_layout(
                            title='Monthly Volume and Success Rate Trends',
                            yaxis=dict(
                                title='Volume (KES Millions)',
                                titlefont=dict(color='rgba(26, 118, 255, 0.8)'),
                                tickfont=dict(color='rgba(26, 118, 255, 0.8)')
                            ),
                            yaxis2=dict(
                                title='Success Rate (%)',
                                titlefont=dict(color='rgba(255, 128, 0, 0.8)'),
                                tickfont=dict(color='rgba(255, 128, 0, 0.8)'),
                                overlaying='y',
                                side='right',
                                range=[0, 100]
                            ),
                            height=400,
                            margin=dict(l=50, r=50, t=50, b=30),
                            legend=dict(
                                orientation="h",
                                y=1.1,
                                x=0.5,
                                xanchor='center'
                            )
                        )
                    ),
                    html.Div([
                        html.P([
                            "Peak Month: December ",
                            html.Span(
                                f"(KES {monthly_data['Volume'].max()/1e6:.1f}M, {monthly_data['Success_Rate'].max():.1f}% success rate)",
                                className="text-muted"
                            )
                        ], className="mb-0 mt-3 regular-text text-center")
                    ])
                ])
            ], className="shadow-sm")
        ], width=12)
    ], className="mb-4"),

    # Success Rate Gauge and User Activity
    dbc.Row([
        # Success Rate Gauge
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Success Rate Performance"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=go.Figure(
                            go.Indicator(
                                mode="gauge+number",
                                value=monthly_data['Success_Rate'].mean(),
                                title={"text": "Average Success Rate",
                                       "font": {"size": 16},
                                       "align": "center"},
                                number={"suffix": "%",
                                       "font": {"size": 28}},
                                gauge={
                                    'axis': {'range': [0, 100]},
                                    'bar': {'color': "#90EE90"},
                                    'steps': [
                                        {'range': [0, 75], 'color': 'rgba(144, 238, 144, 0.2)'},
                                        {'range': [75, 85], 'color': 'rgba(144, 238, 144, 0.4)'},
                                        {'range': [85, 100], 'color': 'rgba(144, 238, 144, 0.6)'}
                                    ],
                                    'threshold': {
                                        'line': {'color': "red", 'width': 2},
                                        'thickness': 0.75,
                                        'value': monthly_data['Success_Rate'].mean()
                                    }
                                }
                            )
                        ).update_layout(
                            height=300,
                            margin=dict(l=30, r=30, t=30, b=30)
                        )
                    )
                ])
            ], className="shadow-sm")
        ], width=4),

        # User Activity Metrics
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("User Activity Metrics"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=go.Figure(data=[
                            go.Scatter(
                                x=[0.2, 0.5, 0.8],
                                y=[1.15, 1.15, 1.15],
                                mode='text',
                                text=['🌍', '👥', '👤'],
                                textfont=dict(size=24),
                                hoverinfo='none',
                                showlegend=False
                            ),
                            go.Scatter(
                                x=[0.2, 0.5, 0.8],
                                y=[1, 1, 1],
                                mode='text',
                                text=['Active Countries', 'Total Remitters', 'Total Recipients'],
                                textfont=dict(size=14),
                                hoverinfo='none',
                                showlegend=False
                            ),
                            go.Scatter(
                                x=[0.2, 0.5, 0.8],
                                y=[0.85, 0.85, 0.85],
                                mode='text',
                                text=[
                                    "16",
                                    f"{monthly_data['Unique_Remitters'].sum():,}",
                                    f"{monthly_data['Unique_Recipients'].sum():,}"
                                ],
                                textfont=dict(size=24, color='#2E86C1'),
                                hoverinfo='none',
                                showlegend=False
                            )
                        ]).update_layout(
                            height=300,
                            showlegend=False,
                            xaxis=dict(
                                showgrid=False,
                                zeroline=False,
                                showticklabels=False,
                                range=[0, 1]
                            ),
                            yaxis=dict(
                                showgrid=False,
                                zeroline=False,
                                showticklabels=False,
                                range=[0.5, 1.2]
                            ),
                            margin=dict(l=20, r=20, t=20, b=20),
                            paper_bgcolor='white',
                            plot_bgcolor='white'
                        )
                    )
                ])
            ], className="shadow-sm")
        ], width=8)
    ], className="mb-4"),

    # Daily and Hourly Analysis
    dbc.Row([
        # Daily Transaction Analysis
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Daily Transaction Distribution"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=go.Figure(data=[
                            go.Bar(
                                name='Volume',
                                x=daily_data['Day'],
                                y=daily_data['Volume']/1e6,
                                marker_color='rgba(26, 118, 255, 0.8)',
                                yaxis='y'
                            ),
                            go.Scatter(
                                name='Transactions',
                                x=daily_data['Day'],
                                y=daily_data['Transactions'],
                                mode='lines+markers',
                                marker_color='rgba(255, 128, 0, 0.8)',
                                yaxis='y2'
                            )
                        ]).update_layout(
                            title='Daily Transaction Patterns',
                            yaxis=dict(
                                title='Volume (KES Millions)',
                                titlefont=dict(color='rgba(26, 118, 255, 0.8)'),
                                tickfont=dict(color='rgba(26, 118, 255, 0.8)')
                            ),
                            yaxis2=dict(
                                title='Number of Transactions',
                                titlefont=dict(color='rgb(255, 128, 0)'),
                                tickfont=dict(color='rgb(255, 128, 0)'),
                                overlaying='y',
                                side='right'
                            ),
                            height=350,
                            margin=dict(l=50, r=50, t=50, b=30),
                            legend=dict(
                                orientation="h",
                                y=1.1,
                                x=0.5,
                                xanchor='center'
                            )
                        )
                    ),
                    html.Div([
                        html.P([
                            "Peak Day: Friday ",
                            html.Span(
                                f"(KES {daily_data['Volume'].max()/1e6:.1f}M, {daily_data['Transactions'].max():,} transactions)",
                                className="text-muted"
                            )
                        ], className="mb-0 mt-3 regular-text")
                    ])
                ])
            ], className="shadow-sm")
        ], width=6),
        
        # Hourly Transaction Pattern
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Hourly Transaction Pattern"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=go.Figure(data=[
                            go.Scatter(
                                x=hourly_data['Hour'],
                                y=hourly_data['Volume']/1e6,
                                mode='lines+markers',
                                name='Volume',
                                marker=dict(
                                    size=6,
                                    color='rgba(26, 118, 255, 0.8)'
                                ),
                                line=dict(
                                    width=2,
                                    color='rgba(26, 118, 255, 0.8)'
                                ),
                                yaxis='y'
                            ),
                            go.Scatter(
                                x=hourly_data['Hour'],
                                y=hourly_data['Count'],
                                mode='lines+markers',
                                name='Transaction Count',
                                marker=dict(
                                    size=6,
                                    color='rgba(255, 128, 0, 0.8)'
                                ),
                                line=dict(
                                    width=2,
                                    color='rgba(255, 128, 0, 0.8)'
                                ),
                                yaxis='y2'
                            )
                        ]).update_layout(
                            title='Hourly Volume and Transaction Count Distribution',
                            xaxis_title='Hour of Day',
                            yaxis=dict(
                                title='Volume (KES Millions)',
                                titlefont=dict(color='rgba(26, 118, 255, 0.8)'),
                                tickfont=dict(color='rgba(26, 118, 255, 0.8)')
                            ),
                            yaxis2=dict(
                                title='Number of Transactions',
                                titlefont=dict(color='rgba(255, 128, 0, 0.8)'),
                                tickfont=dict(color='rgba(255, 128, 0, 0.8)'),
                                overlaying='y',
                                side='right'
                            ),
                            height=350,
                            margin=dict(l=50, r=50, t=50, b=100),
                            legend=dict(
                                orientation="h",
                                y=1.1,
                                x=0.5,
                                xanchor='center'
                            ),
                            xaxis=dict(
                                tickangle=-45,
                                tickmode='array',
                                ticktext=hourly_data['Hour'],
                                tickvals=list(range(len(hourly_data)))
                            )
                        )
                    ),
                    html.Div([
                        html.P([
                            "Peak Volume: 2:30 PM ",
                            html.Span(
                                f"(KES {hourly_data['Volume'].max()/1e6:.1f}M)",
                                className="text-muted"
                            ),
                            html.Br(),
                            "Peak Transactions: 11:30 AM ",
                            html.Span(
                                f"({hourly_data['Count'].max():,} transactions)",
                                className="text-muted"
                            )
                        ], className="mb-0 mt-3 regular-text")
                    ])
                ])
            ], className="shadow-sm")
        ], width=6)
    ], className="mb-4"),

    # Industry and Geographic Distribution
    dbc.Row([
        # Industry Analysis
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Transaction Volume by Industry"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=go.Figure(
                            go.Treemap(
                                labels=industry_data['Industry'],
                                parents=[''] * len(industry_data),
                                values=industry_data['Volume'],
                                textinfo='label+value+percent parent',
                                hovertemplate=(
                                    "<b>%{label}</b><br>" +
                                    "Volume: KES %{value:,.2f}<br>" +
                                    "Share: %{percentParent:.1%}<extra></extra>"
                                ),
                                marker=dict(
                                    colors=industry_data['Volume'],
                                    colorscale='Viridis',
                                    showscale=True
                                ),
                                textfont=dict(size=13)
                            )
                        ).update_layout(
                            height=450,
                            margin=dict(l=20, r=20, t=40, b=20)
                        )
                    ),
                    html.Div([
                        html.P([
                            "Largest Industry: Other ",
                            html.Span(
                                f"(KES {industry_data['Volume'].max()/1e9:.2f}B)",
                                className="text-muted"
                            )
                        ], className="mb-0 mt-3 regular-text")
                    ])
                ])
            ], className="shadow-sm")
        ], width=6),
        
        # Geographic Distribution
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Geographic Distribution"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=go.Figure(data=[
                            go.Bar(
                                name='Volume (KES)',
                                x=country_data['Country'],
                                y=country_data['Volume_KES']/1e6,
                                marker_color='rgba(26, 118, 255, 0.8)',
                                yaxis='y'
                            ),
                            go.Scatter(
                                name='Transactions',
                                x=country_data['Country'],
                                y=country_data['Transactions'],
                                mode='lines+markers',
                                marker=dict(
                                    size=8,
                                    color='rgba(255, 128, 0, 0.8)'
                                ),
                                line=dict(
                                    width=2,
                                    color='rgba(255, 128, 0, 0.8)'
                                ),
                                yaxis='y2'
                            )
                        ]).update_layout(
                            title='Country-wise Distribution',
                            yaxis=dict(
                                title='Volume (KES Millions)',
                                type='log',
                                titlefont=dict(color='rgba(26, 118, 255, 0.8)'),
                                tickfont=dict(color='rgba(26, 118, 255, 0.8)')
                            ),
                            yaxis2=dict(
                                title='Number of Transactions',
                                type='log',
                                overlaying='y',
                                side='right',
                                titlefont=dict(color='rgba(255, 128, 0, 0.8)'),
                                tickfont=dict(color='rgba(255, 128, 0, 0.8)')
                            ),
                            xaxis_tickangle=-45,
                            height=450,
                            margin=dict(l=50, r=50, t=50, b=100),
                            legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="center",
                                x=0.5
                            )
                        )
                    ),
                    html.Div([
                        html.P([
                            "Top Country: United Kingdom ",
                            html.Span(
                                f"(KES {country_data['Volume_KES'].max()/1e9:.2f}B, {country_data['Transactions'].max():,} transactions)",
                                className="text-muted"
                            )
                        ], className="mb-0 mt-3 regular-text")
                    ])
                ])
            ], className="shadow-sm")
        ], width=6)
    ], className="mb-4"),

    # Client Market Share and Failure Analysis
    dbc.Row([
        # Client Market Share
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Client Market Share"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=go.Figure(
                            data=[go.Pie(
                                labels=client_data['Client'],
                                values=client_data['Volume'],
                                textinfo='label+percent',
                                hovertemplate=(
                                    "<b>%{label}</b><br>" +
                                    "Volume: KES %{value:,.2f}<br>" +
                                    "Share: %{percent}<extra></extra>"
                                ),
                                hole=0.3
                            )]
                        ).update_layout(
                            height=400,
                            margin=dict(l=20, r=20, t=40, b=20),
                            legend=dict(orientation="h", yanchor="bottom", y=-0.5)
                        )
                    ),
                    html.Div([
                        *[
                            html.Img(
                                src=f'/assets/{CLIENT_LOGOS.get(client, "Others.jpg")}',
                                id=f'client-logo-{client}',
                                style={
                                    'maxWidth': '80px',
                                    'maxHeight': '40px',
                                    'width': 'auto',
                                    'height': 'auto',
                                    'objectFit': 'contain',
                                    'margin': '5px',
                                    'padding': '5px',
                                    'backgroundColor': '#f8f9fa',
                                    'borderRadius': '5px'
                                }
                            ) for client in client_data['Client']
                        ]
                    ], style={
                        'display': 'flex',
                        'flexWrap': 'wrap',
                        'justifyContent': 'center',
                        'alignItems': 'center',
                        'marginTop': '20px'
                    })
                ])
            ], className="shadow-sm")
        ], width=6),
        
        # Failure Analysis
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Annual Failure Analysis"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=go.Figure(
                            go.Treemap(
                                labels=failure_data['Reason'],
                                parents=[''] * len(failure_data),
                                values=failure_data['Count'],
                                textinfo='label+value+percent parent',
                                hovertemplate=(
                                    "<b>%{label}</b><br>" +
                                    "Count: %{value}<br>" +
                                    "Percentage: %{percentParent:.1%}<extra></extra>"
                                ),
                                marker=dict(
                                    colors=failure_data['Count'],
                                    colorscale=[[0, '#ffebee'], [1, '#c62828']],  # Red scale
                                    showscale=True
                                ),
                                textfont=dict(size=13)
                            )
                        ).update_layout(
                            height=400,
                            margin=dict(l=20, r=20, t=40, b=20)
                        )
                    ),
                    html.Div([
                        html.P([
                            "Total Failed Transactions: ",
                            html.Span(
                                f"{failure_data['Count'].sum():,}",
                                className="font-weight-bold"
                            )
                        ], className="mb-0 mt-3 regular-text text-center")
                    ])
                ])
            ], className="shadow-sm")
        ], width=6)
    ], className="mb-4"),

    # Bank Recipients Analysis
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Bank Recipients Analysis"),
                dbc.CardBody([
                    dbc.Row([
                        # Treemap visualization
                        dbc.Col([
                            dcc.Graph(
                                figure=go.Figure(
                                    go.Treemap(
                                        labels=recipients_data['Bank'],
                                        parents=[''] * len(recipients_data),
                                        values=recipients_data['Volume'],
                                        textinfo='label+value+percent parent',
                                        hovertemplate=(
                                            "<b>%{label}</b><br>" +
                                            "Volume: KES %{value:,.2f}<br>" +
                                            "Market Share: %{percentParent:.1%}<br>" +
                                            "<extra></extra>"
                                        ),
                                        marker=dict(
                                            colors=recipients_data['Volume'],
                                            colorscale='Blues',
                                            showscale=True
                                        ),
                                        textfont=dict(size=13)
                                    )
                                ).update_layout(
                                    height=400,
                                    margin=dict(l=20, r=20, t=20, b=20)
                                )
                            )
                        ], width=9),
                        
                        # Bank logos column
                        dbc.Col([
                            html.Div([
                                *[
                                    html.Div([
                                        html.Img(
                                            src=f'/assets/{BANK_LOGOS.get(bank, "bank_default.png")}',
                                            id=f'bank-logo-{bank}',
                                            style={
                                                'maxWidth': '120px',
                                                'maxHeight': '50px',
                                                'width': 'auto',
                                                'height': 'auto',
                                                'objectFit': 'contain',
                                                'margin': '5px',
                                                'backgroundColor': '#f8f9fa',
                                                'borderRadius': '5px',
                                                'padding': '5px'
                                            }
                                        ),
                                        html.Div([
                                            f"KES {recipients_data.loc[recipients_data['Bank'] == bank, 'Volume'].iloc[0]/1e6:.1f}M",
                                            html.Br(),
                                            f"({recipients_data.loc[recipients_data['Bank'] == bank, 'Market_Share'].iloc[0]:.1f}%)"
                                        ], className="text-muted small text-center")
                                    ], style={
                                        'marginBottom': '15px',
                                        'display': 'flex',
                                        'flexDirection': 'column',
                                        'alignItems': 'center'
                                    }) for bank in recipients_data['Bank']
                                ]
                            ], style={
                                'display': 'flex',
                                'flexDirection': 'column',
                                'justifyContent': 'space-around',
                                'height': '100%',
                                'padding': '10px',
                                'overflowY': 'auto',
                                'maxHeight': '400px'
                            })
                        ], width=3)
                    ])
                ])
            ], className="shadow-sm")
        ], width=12)
    ], className="mb-4"),

], fluid=True, className="p-4")

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run_server(debug=False, host='0.0.0.0', port=port)

    
