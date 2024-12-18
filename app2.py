import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html
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

# Create DataFrames with the data
monthly_data = pd.DataFrame({
    'Metric': ['Total Transactions', 'Transaction Volume (KES)', 'Successful Transactions', 
               'Failed Transactions', 'Success Rate (%)', 'Unique Remitters', 
               'Unique Recipients', 'Unique Countries'],
    'October': [2147, 53713252.25, 2082, 65, 97.0, 987, 740, 6],
    'November': [3623, 74217693.61, 2794, 829, 77.12, 1270, 945, 7],
    'Net Change': [1476, 20504441.36, 712, 764, -19.85, 283, 205, 1],
    'Change %': [68.75, 38.17, 34.20, 1175.38, -20.47, 28.67, 27.70, 16.67]
})

failure_data = pd.DataFrame({
    'Reason': ['Insufficient Balance', 'Other', 'System Error', 'Invalid Account', 
               'Invalid Details', 'General Failure', 'SOAP Error'],
    'Count': [743, 28, 27, 25, 3, 2, 1],
    'Percentage': [89.6, 3.4, 3.3, 3.0, 0.4, 0.2, 0.1]
})

country_data = pd.DataFrame({
    'Country': ['United Kingdom', 'United States', 'Canada', 'Kenya', 'Tanzania', 'Nigeria', 'Ireland'],
    'Volume_KES': [39205310.87, 27361525.15, 3819252.06, 3529435.69, 276744.01, 14050.83, 11375.00],
    'Transactions': [1520, 870, 187, 208, 4, 3, 2]
})

category_data = pd.DataFrame({
    'Category': ['Banking', 'Other', 'Savings', 'Securities & Insurance', 'Retail & Grocery',
                'Real Estate', 'Energy & Heavy Industry', 'Hospitality', 'Medical', 'Government',
                'Religious', 'Education', 'Telco & Tech'],
    'Amount': [41087679.23, 10946152.12, 10078434.28, 4377020.59, 3864372.86,
              743588.00, 207532.04, 761827.55, 956800.17, 316738.20,
              625748.03, 218467.00, 33333.54]
})

# Top 5 by Category Data
top_5_by_category = {
    'Banking': [
        ('EQUITY BANK', 8431804.50),
        ('KCB BANK', 7507623.85),
        ('IM BANK', 4628412.47),
        ('NCBA BANK', 4195733.53),
        ('FAMILY BANK', 3421604.24)
    ],
    'Other': [
        ('NAIROBI DECEMBER CONVENTION', 976775.00),
        ('FAIRPRICE ENTERPRISES DAGORETI', 954412.50),
        ('TILE CARPET CENTRE', 864025.00),
        ('LOOP', 451092.00),
        ('HOT POINT APPLIANCES', 379754.40)
    ],
    'Savings': [
        ('KENVERSITY SACCO', 939890.98),
        ('STIMA SACCO', 903764.87),
        ('CIC MMF', 875772.55),
        ('DIMKES SACCO', 718793.60),
        ('HAZINA SACCO', 653496.25)
    ],
    'Securities & Insurance': [
        ('ETICA CAPITAL', 1539530.36),
        ('SANLAM UNIT TRUST', 393174.00),
        ('AIB CAPITAL', 379548.01),
        ('BRITAM LIFE ASSURANCE', 348735.65),
        ('ICEA LION LIFE ASSURANCE', 236731.72)
    ],
    'Retail & Grocery': [
        ('NAFUU CLASSIC GENERAL HARDWARE', 1376040.80),
        ('MWENDANTU STORES', 416050.00),
        ('RACHAEL HARDWARE', 250200.00),
        ('EAGLE HARDWARE DEALERS', 230375.00),
        ('MACHE HARDWARE STORES', 218120.00)
    ]
}

# Convert top 5 data to DataFrame for visualization
top_5_df = pd.DataFrame([
    {'Category': cat, 'Entity': entity, 'Amount': amount}
    for cat in top_5_by_category
    for entity, amount in top_5_by_category[cat]
])

# Create hourly data
hourly_data = pd.DataFrame({
    'Hour': [f'{i:02d}:00' for i in range(24)],
    'Volume': [0] * 24
})
# Set known values
hourly_data.loc[15, 'Volume'] = 860802.12  # 15:00 peak
hourly_data.loc[23, 'Volume'] = 100.00     # 23:00 minimum

# Layout
app.layout = dbc.Container([
    # Header with logo and title
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(src='https://github.com/Tedomari712/mockdash/blob/main/vngrd.PNG?raw=true',
                     className='logo', 
                     style={'height': '150px', 'object-fit': 'contain'})
            ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'padding': '40px', 'marginBottom': '30px', 'width': '100%'}),
            html.H1("November Mobile Wallet Analysis", 
                   className="text-primary text-center mb-4",
                   style={'letterSpacing': '2px'})
        ])
    ]),

    # Key Metrics Cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Total Transactions", className="card-title text-center"),
                    html.H2(f"{monthly_data.loc[0, 'November']:,.0f}", 
                           className="text-primary text-center"),
                    html.P([
                        html.Span("MoM Change: ", className="regular-text"),
                        html.Span(f"{monthly_data.loc[0, 'Change %']}%",
                                className=f"regular-text {'text-danger' if monthly_data.loc[0, 'Change %'] < 0 else 'text-success'}")
                    ], className="text-center")
                ])
            ], className="shadow-sm")
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Success Rate", className="card-title text-center"),
                    html.H2([
                        f"{monthly_data.loc[4, 'November']}",
                        html.Small("%", className="text-muted")
                    ], className="text-primary text-center"),
                    html.P([
                        html.Span("MoM Change: ", className="regular-text"),
                        html.Span(f"{monthly_data.loc[4, 'Change %']}%",
                                className=f"regular-text {'text-danger' if monthly_data.loc[4, 'Change %'] < 0 else 'text-success'}")
                    ], className="text-center")
                ])
            ], className="shadow-sm")
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Volume (KES)", className="card-title text-center"),
                    html.H2(f"{monthly_data.loc[1, 'November']/1e6:.2f}M", 
                           className="text-primary text-center"),
                    html.P([
                        html.Span("MoM Change: ", className="regular-text"),
                        html.Span(f"{monthly_data.loc[1, 'Change %']}%",
                                className=f"regular-text {'text-danger' if monthly_data.loc[1, 'Change %'] < 0 else 'text-success'}")
                    ], className="text-center")
                ])
            ], className="shadow-sm")
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Avg. Transaction", className="card-title text-center"),
                    html.H2(f"{monthly_data.loc[1, 'November']/monthly_data.loc[0, 'November']:,.0f}", 
                           className="text-primary text-center"),
                    html.P([
                        html.Span("KES per transaction", className="regular-text")
                    ], className="text-center text-muted")
                ])
            ], className="shadow-sm")
        ])
    ], className="mb-4"),

    # Daily Stats Card
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Daily Transaction Stats"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=go.Figure(
                            data=[
                                go.Indicator(
                                    mode="number",
                                    value=4526904.18,
                                    number={"prefix": "KES ", "suffix": "",
                                           "valueformat": ",.2f",
                                           "font": {"size": 24}},
                                    title={"text": "Peak Daily Volume",
                                           "font": {"size": 14}},
                                    domain={'x': [0, 0.5], 'y': [0.7, 1]}
                                ),
                                go.Indicator(
                                    mode="number",
                                    value=2473923.12,
                                    number={"prefix": "KES ", "suffix": "",
                                           "valueformat": ",.2f",
                                           "font": {"size": 24}},
                                    title={"text": "Average Daily Volume",
                                           "font": {"size": 14}},
                                    domain={'x': [0.5, 1], 'y': [0.7, 1]}
                                ),
                                go.Indicator(
                                    mode="number",
                                    value=611787.91,
                                    number={"prefix": "KES ", "suffix": "",
                                           "valueformat": ",.2f",
                                           "font": {"size": 24}},
                                    title={"text": "Lowest Daily Volume",
                                           "font": {"size": 14}},
                                    domain={'x': [0.25, 0.75], 'y': [0.4, 0.7]}
                                ),
                                go.Indicator(
                                    mode="gauge+number",
                                    value=77.12,
                                    title={"text": "Success Rate",
                                           "font": {"size": 14}},
                                    gauge={
                                        'axis': {'range': [0, 100]},
                                        'bar': {'color': "rgba(50, 168, 82, 0.8)"},
                                        'steps': [
                                            {'range': [0, 60], 'color': "rgba(255, 99, 71, 0.3)"},
                                            {'range': [60, 80], 'color': "rgba(255, 215, 0, 0.3)"},
                                            {'range': [80, 100], 'color': "rgba(50, 168, 82, 0.3)"}
                                        ],
                                        'threshold': {
                                            'line': {'color': "red", 'width': 2},
                                            'thickness': 0.75,
                                            'value': 77.12
                                        }
                                    },
                                    domain={'x': [0.25, 0.75], 'y': [0, 0.4]}
                                ),
                            ]
                        ).update_layout(
                            height=400,
                            margin=dict(t=30, b=30)
                        )
                    )
                ]),
                dbc.CardFooter([
                    html.P("Peak Volume Day: November 29, 2024", className="regular-text mb-1"),
                    html.P("Lowest Volume Day: November 20, 2024", className="regular-text mb-0")
                ])
            ], className="shadow-sm")
        ], width=4),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Transaction Success Analysis"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=go.Figure(data=[
                            go.Bar(
                                name='Successful',
                                x=['October', 'November'],
                                y=[monthly_data.loc[2, 'October'], monthly_data.loc[2, 'November']],
                                marker_color='rgb(40, 167, 69)'
                            ),
                            go.Bar(
                                name='Failed',
                                x=['October', 'November'],
                                y=[monthly_data.loc[3, 'October'], monthly_data.loc[3, 'November']],
                                marker_color='rgb(220, 53, 69)'
                            )
                        ]).update_layout(
                            barmode='stack',
                            height=400,
                            title="Success vs Failure Comparison"
                        )
                    )
                ])
            ], className="shadow-sm")
        ], width=8)
    ], className="mb-4"),

    # Hourly Distribution and Geographic Distribution
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Hourly Distribution"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=px.line(
                            hourly_data, x='Hour', y='Volume',
                            title='Hourly Transaction Volume'
                        ).update_layout(
                            height=400,
                            yaxis_type="log",
                            showlegend=False
                        )
                    )
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
                            height=400,
                            xaxis_tickangle=-45,
                            legend=dict(orientation="h", yanchor="bottom", y=1.02)
                        )
                    )
                ])
            ], className="shadow-sm")
        ], width=6)
    ], className="mb-4"),

    # Category Overview and Top 5 Breakdown
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Category Overview"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=px.treemap(
                            category_data,
                            path=['Category'],
                            values='Amount',
                            color='Amount',
                            color_continuous_scale='Viridis'
                        ).update_layout(height=400)
                    )
                ])
            ], className="shadow-sm")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Failure Analysis"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=px.pie(
                            failure_data,
                            values='Count',
                            names='Reason',
                            title='Transaction Failures by Reason'
                        ).update_layout(height=400)
                    )
                ])
            ], className="shadow-sm")
        ], width=6)
    ], className="mb-4"),

    # Top 5 by Category
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Top 5 Entities by Category"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=go.Figure(data=[
                            go.Bar(
                                name=category,
                                x=top_5_df[top_5_df['Category'] == category]['Entity'],
                                y=top_5_df[top_5_df['Category'] == category]['Amount'],
                                text=top_5_df[top_5_df['Category'] == category]['Amount'].apply(lambda x: f'KES {x:,.2f}'),
                                textposition='auto',
                            ) for category in top_5_by_category.keys()
                        ]).update_layout(
                            height=600,
                            barmode='group',
                            showlegend=True,
                            legend_title_text='Category',
                            xaxis_tickangle=-45,
                            margin=dict(b=100)
                        )
                    )
                ])
            ], className="shadow-sm")
        ])
    ], className="mb-4"),

], fluid=True, className="p-4")

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run_server(debug=False, host='0.0.0.0', port=port)