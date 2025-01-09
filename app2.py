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

# Create DataFrames with the yearly data
monthly_data = pd.DataFrame({
    'Month': ['January', 'February', 'March', 'April', 'May', 'June', 
             'July', 'August', 'September', 'October', 'November', 'December'],
    'Transactions': [4416, 3709, 4305, 4683, 3325, 2396, 31, 41, 1198, 2147, 3623, 8217],
    'Volume': [296564946.80, 276359353.66, 278039056.61, 280441910.59, 223579836.58, 
               143369486.87, 925.00, 3843.65, 22142455.28, 53713252.25, 74217693.61, 523575404.54],
    'Success_Rate': [96.5, 96.1, 85.2, 91.7, 96.2, 92.0, 38.7, 97.6, 86.6, 97.0, 77.1, 86.8],
    'Unique_Remitters': [2067, 1762, 1688, 2120, 1309, 1169, 3, 4, 529, 987, 1270, 3367],
    'Unique_Recipients': [2241, 2080, 2136, 2381, 1865, 1539, 6, 14, 420, 740, 945, 3858]
})

# Industry data from PDF
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
    'Transactions': [5137, 4597, 4153, 5062, 6718, 4670, 3715]
})

# Hourly distribution data
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

failure_data = pd.DataFrame({
    'Reason': ['Insufficient Balance', 'Other', 'System Error', 'Invalid Account', 
               'Invalid Credit Party', 'Timed Out', 'General Failure', 'SOAP Error', 'Limit Exceeded'],
    'Count': [2216, 592, 437, 251, 83, 133, 23, 6, 2],
    'Percentage': [58.3, 15.6, 11.5, 6.6, 2.2, 3.5, 0.6, 0.2, 0.1]
})

# Detailed country data from PDF
country_data = pd.DataFrame({
    'Country': ['United Kingdom (GBR)', 'United States (USA)', 'Canada (CAN)', 
                'Kenya (KEN)', 'Nigeria (NGA)', 'Tanzania (TZA)', 'UAE',
                'Denmark (DEN)', 'India (IND)'],
    'Volume_KES': [961197746.35, 422501849.21, 68916278.01, 
                   32036111.63, 6352832.02, 391069.01, 51955.00,
                   159767.50, 45998.61],
    'Transactions': [18050, 7906, 1842, 1339, 395, 6, 2, 4, 2]
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

# App Layout
app.layout = dbc.Container([
    # Header with logo and title
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(src='/assets/vngrd.PNG',
                    className='logo', 
                    style={'height': '150px', 'object-fit': 'contain'})
            ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 
                     'padding': '40px', 'marginBottom': '30px', 'width': '100%'}),
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
                    html.H2(f"{monthly_data['Transactions'].sum():,.0f}", 
                           className="text-primary text-center"),
                    html.P([
                        html.Span("Monthly Average: ", className="regular-text"),
                        html.Span(f"{monthly_data['Transactions'].mean():,.0f}",
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
                        f"{monthly_data['Success_Rate'].mean():.1f}",
                        html.Small("%", className="text-muted")
                    ], className="text-primary text-center"),
                    html.P([
                        html.Span("Peak: ", className="regular-text"),
                        html.Span(f"{monthly_data['Success_Rate'].max():.1f}%",
                                className="regular-text text-success")
                    ], className="text-center")
                ])
            ], className="shadow-sm")
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Total Volume (KES)", className="card-title text-center"),
                    html.H2(f"{monthly_data['Volume'].sum()/1e9:.2f}B", 
                           className="text-primary text-center"),
                    html.P([
                        html.Span("Monthly Average: ", className="regular-text"),
                        html.Span(f"KES {monthly_data['Volume'].mean()/1e6:.1f}M",
                                className="regular-text text-success")
                    ], className="text-center")
                ])
            ], className="shadow-sm")
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Total Unique Remitters", className="card-title text-center"),
                    html.H2(f"{monthly_data['Unique_Remitters'].max():,.0f}", 
                           className="text-primary text-center"),
                    html.P([
                        html.Span("Monthly Average: ", className="regular-text"),
                        html.Span(f"{monthly_data['Unique_Remitters'].mean():,.0f}",
                                className="regular-text text-success")
                    ], className="text-center")
                ])
            ], className="shadow-sm")
        ])
    ], className="mb-4"),

# Monthly Trends and Performance
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Monthly Volume Trends"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=go.Figure(data=[
                            go.Bar(
                                name='Volume (KES Millions)',
                                x=monthly_data['Month'],
                                y=monthly_data['Volume']/1e6,
                                marker_color='rgb(40, 167, 69)'
                            ),
                            go.Scatter(
                                name='Success Rate (%)',
                                x=monthly_data['Month'],
                                y=monthly_data['Success_Rate'],
                                yaxis='y2',
                                line=dict(color='rgb(255, 128, 0)', width=2)
                            )
                        ]).update_layout(
                            title='Monthly Volume and Success Rate',
                            yaxis=dict(title='Volume (KES Millions)'),
                            yaxis2=dict(
                                title='Success Rate (%)',
                                overlaying='y',
                                side='right',
                                range=[0, 100]
                            ),
                            height=400,
                            margin=dict(l=50, r=50, t=50, b=50),
                            legend=dict(orientation="h", y=1.1)
                        )
                    ),
                    html.Div([
                        html.P([
                            "Peak Month: December 2024 ",
                            html.Span(f"(KES {monthly_data['Volume'].max()/1e6:.1f}M)",
                                    className="text-muted")
                        ], className="mb-0 mt-3 regular-text")
                    ])
                ])
            ], className="shadow-sm mb-4")
        ], width=12)
    ], className="mb-4"),

    # User Activity Metrics and Success Rate
    dbc.Row([
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
                                },
                                domain={'x': [0.1, 0.9], 'y': [0, 1]}
                            )
                        ).update_layout(
                            height=300,
                            margin=dict(l=30, r=30, t=30, b=30)
                        )
                    )
                ])
            ], className="shadow-sm")
        ], width=4),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader("User Activity Metrics"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=go.Figure(data=[
                            # Icons
                            go.Scatter(
                                x=[0.2, 0.5, 0.8],
                                y=[1.15, 1.15, 1.15],
                                mode='text',
                                text=['🌍', '👥', '👤'],
                                textfont=dict(size=24),
                                hoverinfo='none',
                                showlegend=False
                            ),
                            # Titles
                            go.Scatter(
                                x=[0.2, 0.5, 0.8],
                                y=[1, 1, 1],
                                mode='text',
                                text=['Active Countries', 'Total Remitters', 'Total Recipients'],
                                textfont=dict(size=14),
                                hoverinfo='none',
                                showlegend=False
                            ),
                            # Current Values
                            go.Scatter(
                                x=[0.2, 0.5, 0.8],
                                y=[0.85, 0.85, 0.85],
                                mode='text',
                                text=[str(len(country_data)), 
                                     f"{monthly_data['Unique_Remitters'].sum():,}",
                                     f"{monthly_data['Unique_Recipients'].sum():,}"],
                                textfont=dict(size=24, color='#2E86C1'),
                                hoverinfo='none',
                                showlegend=False
                            ),
                            # Previous Values
                            go.Scatter(
                                x=[0.2, 0.5, 0.8],
                                y=[0.7, 0.7, 0.7],
                                mode='text',
                                text=[f"vs {len(country_data)-1}",
                                     f"vs {monthly_data['Unique_Remitters'].iloc[0]:,}",
                                     f"vs {monthly_data['Unique_Recipients'].iloc[0]:,}"],
                                textfont=dict(size=12, color='#666'),
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
                            legend=dict(orientation="h", y=1.1)
                        )
                    ),
                    html.Div([
                        html.P([
                            "Peak Day: Friday ",
                            html.Span(f"(KES {daily_data['Volume'].max()/1e6:.1f}M, {daily_data['Transactions'].max():,} transactions)",
                                    className="text-muted")
                        ], className="mb-0 mt-3 regular-text")
                    ])
                ])
            ], className="shadow-sm")
        ], width=6),
        
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
                                marker=dict(size=8),
                                line=dict(width=2, color='rgba(26, 118, 255, 0.8)')
                            )
                        ]).update_layout(
                            title='Hourly Volume Distribution',
                            xaxis_title='Hour of Day',
                            yaxis_title='Average Volume (KES Millions)',
                            height=350,
                            margin=dict(l=50, r=50, t=50, b=30),
                            yaxis=dict(type='log'),
                            showlegend=True,
                            legend=dict(orientation="h", y=1.1)
                        )
                    ),
                    html.Div([
                        html.P([
                            "Peak Hour: 11:30 PM ",
                            html.Span(f"(KES {hourly_data['Volume'].max()/1e6:.1f}M)",
                                    className="text-muted")
                        ], className="mb-0 mt-3 regular-text")
                    ])
                ])
            ], className="shadow-sm")
        ], width=6)
    ], className="mb-4"),

# Industry Analysis Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Transaction Volume by Industry"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=go.Figure(go.Treemap(
                            labels=industry_data['Industry'],
                            parents=[''] * len(industry_data),
                            values=industry_data['Volume'],
                            textinfo='label+value',
                            hovertemplate='<b>%{label}</b><br>Volume: KES %{value:,.2f}<extra></extra>'
                        )).update_layout(
                            height=450,
                            margin=dict(l=20, r=20, t=40, b=20)
                        )
                    ),
                    html.Div([
                        html.P([
                            "Top Industry: Other ",
                            html.Span(f"(KES {industry_data['Volume'].max()/1e9:.2f}B)",
                                    className="text-muted")
                        ], className="mb-0 mt-3 regular-text")
                    ])
                ])
            ], className="shadow-sm")
        ], width=6),
        
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
                                marker_color='rgba(26, 118, 255, 0.8)'
                            ),
                            go.Scatter(
                                name='Transactions',
                                x=country_data['Country'],
                                y=country_data['Transactions'],
                                mode='lines+markers',
                                marker_color='rgba(255, 128, 0, 0.8)',
                                yaxis='y2'
                            )
                        ]).update_layout(
                            title='Country-wise Distribution',
                            yaxis=dict(
                                title='Volume (KES Millions)',
                                type='log'
                            ),
                            yaxis2=dict(
                                title='Number of Transactions',
                                overlaying='y',
                                side='right',
                                type='log'
                            ),
                            xaxis_tickangle=-45,
                            height=450,
                            margin=dict(l=50, r=50, t=50, b=100),
                            legend=dict(orientation="h", y=1.1)
                        )
                    )
                ])
            ], className="shadow-sm")
        ], width=6)
    ], className="mb-4"),

# For the Client Market Share section:
# Client Market Share and Failure Analysis
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Client Market Share"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=go.Figure(data=[go.Pie(
                            labels=client_data['Client'],
                            values=client_data['Volume'],
                            textinfo='label+percent',
                            hovertemplate='<b>%{label}</b><br>' +
                                        'Volume: KES %{value:,.2f}<br>' +
                                        'Share: %{percent}<extra></extra>'
                        )]).update_layout(
                            height=400,
                            margin=dict(l=20, r=20, t=40, b=20)
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
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Annual Failure Analysis"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=go.Figure(go.Treemap(
                            labels=failure_data['Reason'],
                            parents=[''] * len(failure_data),
                            values=failure_data['Count'],
                            textinfo='label+value+percent parent',
                            hovertemplate='<b>%{label}</b><br>' +
                                        'Count: %{value}<br>' +
                                        'Percentage: %{percentParent:.1%}<extra></extra>',
                            marker=dict(
                                colors=failure_data['Count'],
                                colorscale='Reds',
                                showscale=True
                            )
                        )).update_layout(
                            height=400,
                            margin=dict(l=20, r=20, t=40, b=20)
                        )
                    )
                ])
            ], className="shadow-sm")
        ], width=6)
    ], className="mb-4")
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Bank Recipients Analysis"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=go.Figure(data=[
                            go.Bar(
                                name='Volume',
                                x=recipients_data['Bank'],
                                y=recipients_data['Volume']/1e6,
                                marker_color='rgba(26, 118, 255, 0.8)',
                                text=recipients_data['Market_Share'].map('{:.1f}%'.format),
                                textposition='auto',
                            )
                        ]).update_layout(
                            title='Bank Recipients Volume Distribution',
                            yaxis=dict(title='Volume (KES Millions)'),
                            xaxis_tickangle=-45,
                            height=400,
                            margin=dict(l=50, r=50, t=50, b=100),
                            showlegend=True
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
