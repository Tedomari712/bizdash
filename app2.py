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

# Add the logo mappings here, after app initialization but before data structures
CLIENT_LOGOS = {
    'Lemfi': 'LEMFI.png',
    'DLocal': 'DLocal.png',
    'Tangent': 'Tangent.jpg',
    'Nala': 'Nala.png',
    'Brij': 'brij.png',
    'Cellulant': 'Cellulant.png',
    'Wapipay':'wapipay.jpg',
    'Others': 'Others.jpg'
}

BANK_LOGOS = {
    'ABSA Bank': 'Absa.png',
    'Cooperative Bank': 'Coop.jpg',
    'DT Bank': 'DTB.png',
    'Equity Bank': 'Equity.png',
    'Family Bank': 'Familybank.jpeg',
    'I&M Bank': 'im.png',
    'KCB Bank': 'KCB.png',
    'NCBA Bank': 'NCBA.png'
}

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
    'Count': [4416, 3709, 4305, 4683, 3325, 2396, 31, 41, 1198, 2147, 3623, 8217],
    'Volume': [296564946.80, 276359353.66, 278039056.61, 280441910.59, 223579836.58, 
               143369486.87, 925.00, 3843.65, 22142455.28, 53713252.25, 74217693.61, 523575404.54],
    'Success_Rate': [96.5, 96.1, 85.2, 91.7, 96.2, 92.0, 38.7, 97.6, 86.6, 97.0, 77.1, 86.8],
    'Unique_Remitters': [2067, 1762, 1688, 2120, 1309, 1169, 3, 4, 529, 987, 1270, 3367],
    'Unique_Recipients': [2241, 2080, 2136, 2381, 1865, 1539, 6, 14, 420, 740, 945, 3858]
})

# Industry data
industry_data = pd.DataFrame({
    'Industry': ['Other', 'Banking', 'Real Estate', 'Savings', 'Securities & Insurance',
                'Retail & Grocery', 'Religious', 'Education', 'Hospitality', 'Medical',
                'Energy & Heavy Industry', 'Government', 'Telco & Tech'],
    'Volume': [1461861363.64, 134495270.02, 30405803.67, 44181713.27, 19007552.35,
               10461967.57, 4470010.73, 4785022.56, 3771930.72, 1829661.46,
               1812760.27, 515721.32, 389141.00]
})

# Daily transaction data
daily_data = pd.DataFrame({
    'Day': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
    'Volume': [276574448.00, 279786235.00, 240526477.00, 328697945.00, 
               397293759.00, 208898138.00, 169167368.00],
    'Count': [5137, 4597, 4153, 5062, 6718, 4670, 3715]
})

# Updated hourly data
hourly_data = pd.DataFrame({
    'Hour': ['12:00:00 AM', '12:30:00 AM', '1:00:00 AM', '1:30:00 AM', '2:00:00 AM', '2:30:00 AM', 
            '3:00:00 AM', '3:30:00 AM', '4:00:00 AM', '4:30:00 AM', '5:00:00 AM', '5:30:00 AM', 
            '6:00:00 AM', '6:30:00 AM', '7:00:00 AM', '7:30:00 AM', '8:00:00 AM', '8:30:00 AM', 
            '9:00:00 AM', '9:30:00 AM', '10:00:00 AM', '10:30:00 AM', '11:00:00 AM', '11:30:00 AM',
            '12:00:00 PM', '12:30:00 PM', '1:00:00 PM', '1:30:00 PM', '2:00:00 PM', '2:30:00 PM',
            '3:00:00 PM', '3:30:00 PM', '4:00:00 PM', '4:30:00 PM', '5:00:00 PM', '5:30:00 PM',
            '6:00:00 PM', '6:30:00 PM', '7:00:00 PM', '7:30:00 PM', '8:00:00 PM', '8:30:00 PM',
            '9:00:00 PM', '9:30:00 PM', '10:00:00 PM', '10:30:00 PM', '11:00:00 PM', '11:30:00 PM'],
    'Volume': [23923595.64, 28073570.30, 20093102.50, 18651483.10, 20284409.18, 18327660.92,
              21046999.52, 18624234.82, 17169134.74, 15938434.62, 16470431.39, 18256504.64,
              14473250.50, 16664174.87, 21174240.02, 24384442.52, 28430233.46, 35683605.96,
              32293483.80, 33624440.10, 35471112.12, 41021127.01, 42365401.43, 47930870.44,
              38029682.04, 41993842.60, 43313929.16, 35436329.29, 34235004.81, 47425583.34,
              39225509.52, 40058302.81, 34244174.47, 35949800.94, 31541304.54, 34645475.68,
              42870360.52, 41022579.30, 40635039.28, 33436334.89, 42422933.78, 45150244.19,
              35818593.44, 29583004.24, 33139351.87, 31088863.08, 29389421.09, 32641760.13],
    'Count': [456, 443, 433, 365, 354, 325, 421, 277, 309, 327, 309, 285,
              246, 287, 298, 356, 392, 495, 478, 480, 524, 598, 669, 897,
              593, 651, 658, 630, 627, 695, 648, 654, 591, 602, 639, 602,
              597, 642, 677, 588, 704, 711, 588, 494, 513, 463, 444, 503]
})

# Failure data
failure_data = pd.DataFrame({
    'Reason': ['Insufficient Balance', 'Other', 'System Error', 'Invalid Account', 
               'Invalid Credit Party', 'Timed Out', 'General Failure', 'SOAP Error', 'Limit Exceeded'],
    'Count': [2216, 592, 437, 251, 83, 133, 23, 6, 2],
    'Percentage': [58.3, 15.6, 11.5, 6.6, 2.2, 3.5, 0.6, 0.2, 0.1]
})

# Country data
country_data = pd.DataFrame({
    'Country': ['United Kingdom (GBR)', 'United States (USA)', 'Canada (CAN)', 
                'Kenya (KEN)', 'Nigeria (NGA)', 'Tanzania (TZA)', 'UAE',
                'Denmark (DEN)', 'India (IND)'],
    'Volume_KES': [961197746.35, 422501849.21, 68916278.01, 
                   32036111.63, 6352832.02, 391069.01, 51955.00,
                   159767.50, 45998.61],
    'Transactions': [18050, 7906, 1842, 1339, 395, 6, 2, 4, 2]
})

# Client data
client_data = pd.DataFrame({
    'Client': ['Lemfi', 'DLocal', 'Tangent', 'Nala', 'Wapipay', 'Brij', 
              'Cellulant', 'Others'],
    'Volume': [1701947843.25, 410741870.10, 31148619.48, 13119614.16, 
              15022090.45, 28085.00, 43.00, 0.00],
    'Transactions': [29281, 4547, 203, 173, 42, 42, 4, 0],
    'Market_Share': [78.36, 18.91, 1.43, 0.60, 0.69, 0.01, 0.00, 0.00]
})

# Bank recipients data
recipients_data = pd.DataFrame({
    'Bank': ['ABSA Bank', 'Cooperative Bank', 'DT Bank', 'Equity Bank', 
            'Family Bank', 'I&M Bank', 'KCB Bank', 'NCBA Bank'],
    'Volume': [7282025.65, 11802956.97, 7677251.81, 24819864.19,
              9481656.86, 9501100.76, 17038871.74, 11536537.68],
    'Transactions': [139, 338, 124, 889, 215, 244, 348, 195],
    'Market_Share': [6.53, 10.58, 6.88, 22.25, 8.50, 8.52, 15.27, 10.34]
})

# Start App Layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(
                    src='/assets/vngrd.PNG',
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
                "2024 Annual Business Transfer Analysis", 
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
                        f"{monthly_data['Count'].sum():,.0f}", 
                        className="text-primary text-center"
                    ),
                    html.P([
                        html.Span("Monthly Average: ", className="regular-text"),
                        html.Span(
                            f"{monthly_data['Count'].mean():,.0f}",
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
                            f"KES {monthly_data['Volume'].mean()/1e6:.1f}M",
                            className="regular-text text-success"
                        )
                    ], className="text-center")
                ])
            ], className="shadow-sm")
        ]),
        
        # Unique Remitters Card
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
                                y=daily_data['Count'],
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
                                f"(KES {daily_data['Volume'].max()/1e6:.1f}M, {daily_data['Count'].max():,} transactions)",
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
