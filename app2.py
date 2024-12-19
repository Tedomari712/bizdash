# Import required libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output  # Added this line
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
    'Country': ['United Kingdom', 'United States of America', 'Canada', 
                'Kenya', 'Tanzania', 'Nigeria', 'Ireland'],
    'Volume_KES': [39205310.87, 27361525.15, 3819252.06, 
                   3529435.69, 276744.01, 14050.83, 11375.00],
    'Transactions': [1520, 870, 187, 208, 4, 3, 2]
})

# Category data
category_data = pd.DataFrame({
    'Category': ['Banking', 'Other', 'Savings', 'Securities & Insurance', 
                'Retail & Grocery', 'Real Estate', 'Energy & Heavy Industry',
                'Hospitality', 'Medical', 'Government', 'Religious',
                'Education', 'Telco & Tech'],
    'Amount': [41087679.23, 10946152.12, 10078434.28, 4377020.59,
               3864372.86, 743588.00, 207532.04, 761827.55,
               956800.17, 316738.20, 625748.03, 218467.00, 33333.54]
})

# Top 5 entities data structure for all categories
top5_data = {
    'Banking': {
        'Entity': ['EQUITY BANK', 'KCB BANK', 'IM BANK', 'NCBA BANK', 'FAMILY BANK'],
        'Amount': [8431804.50, 7507623.85, 4628412.47, 4195733.53, 3421604.24]
    },
    'Other': {
        'Entity': ['NAIROBI DECEMBER CONVENTION', 'FAIRPRICE ENTERPRISES DAGORETI', 
                  'TILE CARPET CENTRE', 'LOOP', 'HOT POINT APPLIANCES'],
        'Amount': [976775.00, 954412.50, 864025.00, 451092.00, 379754.40]
    },
    'Savings': {
        'Entity': ['KENVERSITY SACCO', 'STIMA SACCO', 'CIC MMF', 'DIMKES SACCO', 'HAZINA SACCO'],
        'Amount': [939890.98, 903764.87, 875772.55, 718793.60, 653496.25]
    },
    'Securities & Insurance': {
        'Entity': ['ETICA CAPITAL', 'SANLAM UNIT TRUST', 'AIB CAPITAL', 
                  'BRITAM LIFE ASSURANCE', 'ICEA LION LIFE ASSURANCE'],
        'Amount': [1539530.36, 393174.00, 379548.01, 348735.65, 236731.72]
    },
    'Retail & Grocery': {
        'Entity': ['NAFUU CLASSIC GENERAL HARDWARE', 'MWENDANTU STORES', 
                  'RACHAEL HARDWARE', 'EAGLE HARDWARE DEALERS', 'MACHE HARDWARE STORES'],
        'Amount': [1376040.80, 416050.00, 250200.00, 230375.00, 218120.00]
    },
    'Real Estate': {
        'Entity': ['AMG REALTORS', 'BUXTON POINT APARTMENT', 'OPTIVEN', 
                  'ICEA LION ASSET MANAGEMENT', 'MUGUMO GREENS MANAGEMENT'],
        'Amount': [296261.00, 156275.00, 148925.50, 68101.50, 36000.00]
    },
    'Energy & Heavy Industry': {
        'Entity': ['CANADIANSOLAR ENERGY', 'JEMYSUN ENERGY SOLUTIONS', 'RUBIS ENERGY', 
                  'KARUNA CORNERSTONE ENERGY', 'SIRIKWA QUARRY'],
        'Amount': [84000.00, 56492.00, 15145.30, 10000.00, 8330.00]
    },
    'Hospitality': {
        'Entity': ['SERENA HOTELS', 'BONFIRE ADVENTURE YALA TOWER', 
                  'BONFIRE ADVENTURES WARWICK', 'PLAZA BEACH HOTEL', 'MERIDIAN HOTEL'],
        'Amount': [412500.00, 98000.00, 72991.00, 40000.00, 27310.50]
    },
    'Medical': {
        'Entity': ['JUBILEE HEALTH INSURANCE', 'JOBS MEDICAL FUND', 
                  'GURU NANAK RAMGARHIA SIKH HOSPITAL', 'AIC KIJABE HOSPITAL', 'FRANCIS COMMUNITY HOSPITAL'],
        'Amount': [173705.67, 172353.00, 124876.00, 101986.00, 81760.00]
    },
    'Government': {
        'Entity': ['ECITIZEN', 'KIAMBU COUNTY GOVERNMENT REVENUE', 
                  'COUNTY HARDWARE AND TIMBER MERCHANTS', 'NAIROBI CITY COUNTY REVENUE', 
                  'MURANGA COUNTY CREAMERIES COOP UNION'],
        'Amount': [166508.00, 123469.08, 15881.12, 10000.00, 880.00]
    },
    'Religious': {
        'Entity': ['CRY OF THE SPIRIT MINISTRY', 'DELIVERANCE CHURCH', 
                  'RUIRU CATHOLIC FUND', 'PARKLANDS BAPTIST CHURCH', 'FAITH EVANGELISTIC MINISTRY'],
        'Amount': [77100.00, 75174.00, 67599.23, 54315.00, 50750.00]
    },
    'Education': {
        'Entity': ['DAYSTAR UNIVERSITY', 'KABARAK UNIVERSITY', 'MOUNT UNIVERSITY', 
                  'CLARES KAPLONG SCHOOL OF NURSING', 'BORN TO LEAD ACADEMY'],
        'Amount': [104640.00, 48850.00, 39812.00, 8150.00, 4500.00]
    },
    'Telco & Tech': {
        'Entity': ['SAFARICOM POST PAID', 'SAFARICOM RETAIL KIMATHI', 'MTAANI TELECOM', 
                  'KONNECT DATA NETWORKS', 'VILCOM NETWORKS'],
        'Amount': [17030.00, 5150.00, 4000.00, 2000.00, 1999.00]
    }
}

# Create a DataFrame for hourly data
hourly_data = pd.DataFrame({
    'Hour': [f'{i:02d}:00' for i in range(24)],
    'Volume': np.random.exponential(scale=5000000, size=24)
})
# Set known peak and minimum
hourly_data.loc[15, 'Volume'] = 860802.12  # 3:00 PM peak
hourly_data.loc[23, 'Volume'] = 100.00     # 11:00 PM minimum

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
            html.H1("November Business Transfer Analysis", 
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
                        html.Span(f"+{monthly_data.loc[0, 'Change %']}%",
                                className="regular-text text-success")
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
                                className="regular-text text-danger")
                    ], className="text-center")
                ])
            ], className="shadow-sm")
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Volume (KES)", className="card-title text-center"),
                    html.H2(f"{monthly_data.loc[1, 'November']/1e6:.1f}M", 
                           className="text-primary text-center"),
                    html.P([
                        html.Span("MoM Change: ", className="regular-text"),
                        html.Span(f"+{monthly_data.loc[1, 'Change %']}%",
                                className="regular-text text-success")
                    ], className="text-center")
                ])
            ], className="shadow-sm")
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Unique Remitters", className="card-title text-center"),
                    html.H2(f"{monthly_data.loc[5, 'November']:,.0f}", 
                           className="text-primary text-center"),
                    html.P([
                        html.Span("MoM Change: ", className="regular-text"),
                        html.Span(f"+{monthly_data.loc[5, 'Change %']}%",
                                className="regular-text text-success")
                    ], className="text-center")
                ])
            ], className="shadow-sm")
        ])
    ], className="mb-4"),

    # Main Charts Row
    dbc.Row([
        # Left Column
        dbc.Col([
            # Daily Transaction Volume Card
            dbc.Card([
                dbc.CardHeader("Daily Transaction Volume"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=go.Figure(
                            data=[
                                go.Indicator(
                                    mode="number",
                                    value=4.53,  # Peak daily volume
                                    number={"prefix": "KES ", "suffix": "M",
                                           "valueformat": ".1f",
                                           "font": {"size": 24}},
                                    title={"text": "Peak Daily Volume",
                                           "font": {"size": 14},
                                           "align": "center"},
                                    domain={'x': [0.05, 0.45], 'y': [0.65, 0.95]}
                                ),
                                go.Indicator(
                                    mode="number",
                                    value=2.47,  # Average daily volume
                                    number={"prefix": "KES ", "suffix": "M",
                                           "valueformat": ".1f",
                                           "font": {"size": 24}},
                                    title={"text": "Average Daily Volume",
                                           "font": {"size": 14},
                                           "align": "center"},
                                    domain={'x': [0.55, 0.95], 'y': [0.65, 0.95]}
                                ),
                                go.Indicator(
                                    mode="number",
                                    value=829,  # Peak daily transactions
                                    number={"valueformat": ",",
                                           "font": {"size": 24}},
                                    title={"text": "Peak Daily Transactions",
                                           "font": {"size": 14},
                                           "align": "center"},
                                    domain={'x': [0.05, 0.45], 'y': [0.375, 0.625]}
                                ),
                                go.Indicator(
                                    mode="number",
                                    value=121,
                                    number={"valueformat": ",",
                                           "font": {"size": 24}},
                                    title={"text": "Average Daily Transactions",
                                           "font": {"size": 14},
                                           "align": "center"},
                                    domain={'x': [0.55, 0.95], 'y': [0.375, 0.625]}
                                ),
                                go.Indicator(
                                    mode="gauge+number",
                                    value=77.12,  # Success rate
                                    title={"text": "Daily Success Rate",
                                           "font": {"size": 16},
                                           "align": "center"},
                                    number={"suffix": "%",
                                           "font": {"size": 28}},
                                    gauge={
                                        'axis': {'range': [0, 100]},
                                        'bar': {'color': "rgb(255, 215, 0)"},
                                        'steps': [
                                            {'range': [0, 75], 'color': 'rgba(255, 215, 0, 0.2)'},
                                            {'range': [75, 85], 'color': 'rgba(255, 215, 0, 0.4)'},
                                            {'range': [85, 100], 'color': 'rgba(255, 215, 0, 0.6)'}
                                        ],
                                        'threshold': {
                                            'line': {'color': "red", 'width': 2},
                                            'thickness': 0.75,
                                            'value': 77.12
                                        }
                                    },
                                    domain={'x': [0.15, 0.85], 'y': [0.02, 0.32]}
                                )
                            ]
                        ).update_layout(
                            height=550,
                            margin=dict(t=30, b=30, l=30, r=30)
                        )
                    )
                ]),
                dbc.CardFooter([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.P("Peak Volume Day: November 29, 2024", className="regular-text mb-1"),
                                html.P("Lowest Volume Day: November 20, 2024 (KES 612K)", className="regular-text mb-0")
                            ])
                        ])
                    ], className="small")
                ])
            ], className="shadow-sm mb-4"),

            # Hourly Distribution Card
            dbc.Card([
                dbc.CardHeader("Hourly Distribution"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=px.line(
                            hourly_data, x='Hour', y='Volume',
                            title='Hourly Transaction Volume'
                        ).update_layout(
                            yaxis_type="log",
                            showlegend=False,
                            height=300
                        )
                    )
                ])
            ], className="shadow-sm")
        ], width=4),

        # Right Column
        dbc.Col([
            # Transaction Success Analysis Card
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
                            height=550,
                            title="Success vs Failure Comparison"
                        )
                    )
                ])
            ], className="shadow-sm mb-4"),
            
            # User Activity Metrics Card
            dbc.Card([
                dbc.CardHeader("User Activity Metrics"),
                dbc.CardBody([
                    dcc.Graph(
                        figure=go.Figure(data=[
                            # First row - Icons
                            go.Scatter(
                                x=[0.2, 0.5, 0.8],
                                y=[1.15, 1.15, 1.15],
                                mode='text',
                                text=['🌍', '👥', '👤'],
                                textfont=dict(size=24),
                                hoverinfo='none',
                                showlegend=False
                            ),
                            # Second row - Titles
                            go.Scatter(
                                x=[0.2, 0.5, 0.8],
                                y=[1, 1, 1],
                                mode='text',
                                text=['Active Countries', 'Unique Remitters', 'Unique Recipients'],
                                textfont=dict(size=14),
                                hoverinfo='none',
                                showlegend=False
                            ),
                            # Third row - Current Values
                            go.Scatter(
                                x=[0.2, 0.5, 0.8],
                                y=[0.85, 0.85, 0.85],
                                mode='text',
                                text=['7', '1,270', '945'],
                                textfont=dict(size=24, color='#2E86C1'),
                                hoverinfo='none',
                                showlegend=False
                            ),
                            # Fourth row - Previous Values
                            go.Scatter(
                                x=[0.2, 0.5, 0.8],
                                y=[0.7, 0.7, 0.7],
                                mode='text',
                                text=['vs 6', 'vs 987', 'vs 740'],
                                textfont=dict(size=12, color='#666'),
                                hoverinfo='none',
                                showlegend=False
                            ),
                            # Fifth row - Change Percentage
                            go.Scatter(
                                x=[0.2, 0.5, 0.8],
                                y=[0.6, 0.6, 0.6],
                                mode='text',
                                text=['+16.67%', '+28.67%', '+27.70%'],
                                textfont=dict(
                                    size=14,
                                    color=['#28a745', '#28a745', '#28a745']
                                ),
                                hoverinfo='none',
                                showlegend=False
                            )
                        ]).update_layout(
                            height=350,
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
                dbc.CardHeader("Failure Analysis"),
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
                    html.Img(
                        src='/assets/LEMFI.png',
                        style={
                            'width': '50%',
                            'display': 'block',
                            'margin': 'auto'
                        }
                    ),
                    html.H3(
                        "100% Market Share",
                        className="text-center mt-4",
                        style={'color': '#1a76ff'}
                    ),
                    html.P(
                        f"Total Volume: KES {74217693.61:,.2f}",
                        className="text-center regular-text"
                    ),
                    html.P(
                        "Total Transactions: 2,794",
                        className="text-center regular-text"
                    )
                ])
            ], className="shadow-sm")
        ], width=6)
    ], className="mb-4"),

    # New Category Overview and Top 5 Entities
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
                            color_continuous_scale='Viridis',
                            title='Transaction Volume by Category'
                        ).update_layout(
                            height=500,
                            margin=dict(l=20, r=20, t=40, b=20)
                        )
                    )
                ])
            ], className="shadow-sm")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Top 5 Entities by Category"),
                dbc.CardBody([
                    dcc.Dropdown(
                        id='category-dropdown',
                        options=[{'label': cat, 'value': cat} for cat in top5_data.keys()],
                        value='Banking',  # Default value
                        className='mb-3'
                    ),
                    dcc.Graph(id='top5-graph')
                ])
            ], className="shadow-sm")
        ], width=6)
    ], className="mb-4")

], fluid=True, className="p-4")

# Callback for Top 5 Entities Graph
@app.callback(
    Output('top5-graph', 'figure'),
    Input('category-dropdown', 'value')
)
def update_top5_graph(selected_category):
    data = top5_data[selected_category]
    
    fig = go.Figure(data=[
        go.Bar(
            x=data['Entity'],
            y=data['Amount'],
            marker_color='rgba(26, 118, 255, 0.8)'
        )
    ])
    
    fig.update_layout(
        title=f'Top 5 Entities - {selected_category}',
        xaxis_tickangle=-45,
        height=400,
        margin=dict(l=20, r=20, t=40, b=100),
        yaxis_title='Amount (KES)'
    )
    
    return fig

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run_server(debug=False, host='0.0.0.0', port=port)
