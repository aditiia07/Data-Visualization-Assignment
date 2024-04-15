# %%
# !pip3 install plotly dash

# %%
import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd
# import dash_table
from dash import dash_table
from dash.dependencies import Input, Output, State
# from google.colab import drive
# drive.mount('/content/drive')

# %%
athlete_events = pd.read_csv('athlete_events.csv')
# athlete_events = pd.read_csv(r'C:\Users\abhim\OneDrive\Desktop\Term 2\Data Viz\Project\archive\athlete_events.csv')

# %%
# Calculate the total number of Olympic Games
total_games = athlete_events['Games'].nunique()

# Calculate the total number of unique participants
total_participants = athlete_events['ID'].nunique()

# Prepare data for the Gender Distribution Pie Chart
gender_distribution = athlete_events['Sex'].value_counts().reset_index()
gender_distribution.columns = ['Gender', 'Count']

# Prepare data for the Summer vs. Winter Distribution Pie Chart
season_distribution = athlete_events['Season'].value_counts().reset_index()
season_distribution.columns = ['Season', 'Count']

# Assuming athlete_events is your DataFrame
participants_by_country = athlete_events.groupby('NOC')['ID'].nunique().reset_index(name='Number of Participants')
participants_by_country.sort_values(by='Number of Participants', ascending=False, inplace=True)

# Preparing the participation timeline data
timeline_data = athlete_events.groupby('Year')['ID'].nunique().reset_index(name='Number of Participants')


# %%

# Define initial figure for the timeline graph to show all participation by default
initial_fig = px.line(
    timeline_data,
    x="Year",
    y="Number of Participants",
    title='Olympics Participation Over the Years',
    line_shape='linear',
    color_discrete_sequence=['black']  # Line color changed to black
)
initial_fig.update_traces(line=dict(width=3))  # Line made thicker

# Additional dropdown options
countries_options = [{'label': 'All', 'value': 'All'}] + [{'label': country, 'value': country} for country in athlete_events['NOC'].unique()]
sports_options = [{'label': 'All', 'value': 'All'}] + [{'label': sport, 'value': sport} for sport in athlete_events['Sport'].unique()]
medals_options = [{'label': 'All', 'value': 'All'}, {'label': 'Gold', 'value': 'Gold'}, {'label': 'Silver', 'value': 'Silver'}, {'label': 'Bronze', 'value': 'Bronze'}, {'label': 'None', 'value': 'None'}]

app = dash.Dash(__name__)

common_card_style = {
    'display': 'inline-block',
    'width': '30%',  # Reduced width to make cards smaller
    'margin': '10px',
    'padding': '20px',
    'boxShadow': '0px 0px 0px #ffffff !important',
    'background': 'white',
    # 'borderRadius': '5px',
    'textAlign': 'center',
    'boxSizing': 'border-box',
    'border': '1px solid black'
}
common_card_style['boxSizing'] = 'border-box'

def update_pie_layout(figure):
    figure.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=True  # Change this to True to show the legend
    )
    return figure


dataset_description_card = html.Div([
    html.H4('Exploring the Pinnacle of Sports History Through Data'),
    dcc.Markdown('''
Welcome to our interactive exploration of over a century of Olympic triumphs, challenges, and global participation. This dashboard presents an unprecedented data-driven journey through the chronicles of the Olympic Games, showcasing the tales of athletes and nations as they compete on the world’s foremost stage of sport.

Insights at a Glance:

Uncover trends in Total Number of Unique Participants, reflecting the expanding inclusivity and reach of the games over time.

Explore the Gender Distribution in the Olympics, a mirror to the broader societal shifts towards gender equality in sports.

Engage with the Olympic Participation Over the Years, noting the ebb and flow of global engagement in this international event.

Celebrate the Top 10 Athletes, whose extraordinary feats have left indelible marks on history and view a detailed Selected Athlete Profile, encompassing their Olympic journey from debut to final accolades.
'''),
], style={
    'width': '100%',  # Adjusted width to span the whole page
    'display': 'block',  # Changed from inline-block to block
    'verticalAlign': 'top',
    'margin': '10px auto',
    'padding': '20px',
    'boxShadow': '0px 0px 0px #ffffff !important',
    'background': 'white',
    # 'borderRadius': '5px',
    'textAlign': 'justify',  # Justify align text for better readability
    'boxSizing': 'border-box'
})

common_card_style = {
    'width': '100%',  # Adjusted width to take up less than half of the page
    # Include the rest of your common_card_style properties here
    'display': 'inline-block',
    'margin': '10px',
    'padding': '20px',
    'boxShadow': '0px 0px 0px #ffffff !important',
    'background': 'white',
    # 'borderRadius': '5px',
    'textAlign': 'center',
    'boxSizing': 'border-box',
    'border': '1px solid black'
}

statistics_and_charts_section = html.Div([
    dataset_description_card,  # Moved dataset_description_card to the top
    html.Div([
        # Card for Total Number of Olympic Games
        html.Div([
            html.H4('Total Number of Olympic Games'),
            html.P(str(total_games), style={'fontSize': '2em'}),
            html.H4('Summer vs Winter Games'),
            dcc.Graph(
                id='season-distribution',
                figure=update_pie_layout(px.pie(
                    season_distribution,
                    values='Count',
                    names='Season',
                    title='Summer vs Winter Games',
                    color_discrete_sequence=['#159A9C', '#002333']
                ))
            )
        ], style=common_card_style),

        # Card for Total Number of Unique Participants
        html.Div([
            html.H4('Total Number of Unique Participants'),
            html.P(str(total_participants), style={'fontSize': '2em'}),
            html.H4('Gender Distribution'),
            dcc.Graph(
                id='gender-distribution',
                figure=update_pie_layout(px.pie(
                    gender_distribution,
                    values='Count',
                    names='Gender',
                    title='Gender Distribution',
                    color_discrete_sequence=['#159A9C', '#002333']
                ))
            )
        ], style=common_card_style),
    ], style={
        'display': 'flex',
        'justifyContent': 'space-between',  # Changed from flex-start to space-between to distribute space evenly between the cards
        'alignItems': 'flex-start',  # Changed from center to flex-start to align items to the top
        # 'flexWrap': 'wrap'
    }),
], style={
    'display': 'flex',
    'flexDirection': 'column',  # Added flexDirection to arrange the children vertically
    'justifyContent': 'flex-start',
    # 'alignItems': 'flex-start',
    'flexWrap': 'wrap'
})

# Define the layout of the app
app.layout = html.Div([
    html.Div([
        # Header
        html.H1(
            'A Data Sprint through 120 years of Olympics History',
            style={
                'textAlign': 'center',
                'margin-bottom': '0.5em',
                'fontFamily': 'Raleway, sans-serif',
                'fontSize': '3em',
                'backgroundColor': 'white'
            }
        ),
        # Main content area with filters and graph
        html.Div([ statistics_and_charts_section,
              ], style={'display': 'flexWrap', 'background': '#f0f0f0', 'padding': '20px', 'borderRadius': '5px'}),

        html.Div([
            html.Div([
                html.H3("Filters", style={'color': 'white'}),
                # html.Hr(),
                html.Div([
                    html.Label("Time Period", style={'color': 'white', 'display': 'block'}),
                    dcc.RangeSlider(
                        id='year-range-slider',
                        min=athlete_events['Year'].min(),
                        max=athlete_events['Year'].max(),
                        step=1,
                        marks={year: {'label': str(year), 'style': {'color': '#ffffff'}} for year in range(athlete_events['Year'].min(), athlete_events['Year'].max() + 1, 10)},
                        value=[athlete_events['Year'].min(), athlete_events['Year'].max()],
                        allowCross=False,
                        className="dcc_control"
                    )
                ], style={'color': 'white', 'width': '100%', 'padding': '20px'}),

                html.Label("Season", style={'color': 'white', 'display': 'block'}),
                dcc.Dropdown(
                    id='season-filter',
                    options=[{'label': 'All', 'value': 'All'}] + [{'label': season, 'value': season} for season in ['Summer', 'Winter']],
                    value='All',
                    clearable=False,
                    style={'color': 'black', 'width': '100%'}
                ),
                html.Label("Gender", style={'color': 'white', 'display': 'block'}),
                dcc.Dropdown(
                    id='gender-filter',
                    options=[{'label': 'All', 'value': 'All'}, {'label': 'Male', 'value': 'M'}, {'label': 'Female', 'value': 'F'}],
                    value='All',
                    clearable=False,
                    style={'color': 'black', 'width': '100%'}
                ),
                html.Label("Country", style={'color': 'white', 'display': 'block'}),
                dcc.Dropdown(
                    id='country-filter',
                    options=countries_options,
                    value='All',
                    clearable=False,
                    style={'color': 'black', 'width': '100%'}
                ),
                html.Label("Sport", style={'color': 'white', 'display': 'block'}),
                dcc.Dropdown(
                    id='sport-filter',
                    options=sports_options,
                    value='All',
                    clearable=False,
                    style={'color': 'black', 'width': '100%'}
                ),
                html.Label("Medal", style={'color': 'white', 'display': 'block'}),
                dcc.Dropdown(
                    id='medal-filter',
                    options=medals_options,
                    value='All',
                    clearable=False,
                    style={'color': 'black', 'width': '100%'}
                ),
            ], style={'background-color': '#2E4551', 'padding': '20px', 'width': '100%', 'margin': '10px', 'borderRadius': '5px', 'display': 'flex', 'flexDirection': 'row', 'flexWrap': 'wrap', 'justifyContent': 'space-between'}),
        ], style={'display': 'flex', 'background': '#f0f0f0', 'padding': '20px', 'borderRadius': '0px'}),

        html.Div([
            html.Div([
                dcc.Graph(
                    id='participation-timeline',
                    # Include the figure for your graph here
                    config={'scrollZoom': True, 'displayModeBar': True},
                )
            ], style={'flex': 1, 'padding': '20px', 'margin': '10px', 'borderRadius': '5px', 'border': '2px solid #2E4551', 'width': '100%'}),
        ], style={'display': 'flex', 'background': '#f0f0f0', 'padding': '20px', 'borderRadius': '0px'}),

        html.Div([
            html.Div([
                dcc.Graph(
                    id='top-athletes-chart',
                    config={'displayModeBar': False},  # Remove mode bar for this chart
                ),
            ], style={'flex': 1, 'padding': '20px', 'margin': '10px', 'borderRadius': '5px', 'border': '2px solid #f0f0f0', 'width': '100%'}),
        ], style={'display': 'flex', 'background': '#2E4551', 'padding': '20px', 'borderRadius': '0px'}),

        html.Div([
            html.Div([
                html.H3("Selected Athlete Profile", style={'color': 'black', 'fontFamily': 'Raleway, sans-serif'}),
                html.P("Hover over the graph above to select an athlete.", style={'textAlign': 'center', 'color': 'black'}),
                dash_table.DataTable(id='athlete-profile',
                                    style_header={'backgroundColor': '#003366', 'color': 'white','fontFamily': 'Raleway, sans-serif'})
                # Include the data for your table here
            ], style={'flex': 1, 'padding': '20px', 'margin': '10px', 'borderRadius': '5px', 'border': '2px solid #2E4551', 'width': '100%','fontFamily': 'Raleway, sans-serif'}),
        ], style={'display': 'flex', 'background': '#f0f0f0', 'padding': '20px', 'borderRadius': '5px','fontFamily': 'Raleway, sans-serif'}),

        # Credits area
        html.Div([
            html.H3("Credits", style={'textAlign': 'center', 'color': 'black'}),
            html.P(
                "This dashboard was created by Team Totally Forgot.",
                style={'textAlign': 'center', 'color': 'black'}
            ),
            html.P(
                "Aditi Agarwal, Saptarshi Banerjee, Abhimanyu Bhadauria & Duoer Gu",
                style={'textAlign': 'center', 'color': 'black'}
            ),
        ], style={'background': '#f0f0f0', 'padding': '20px', 'borderRadius': '5px', 'margin-top': '20px'}),

    ], style={'maxWidth': '1400px', 'margin': 'auto', 'padding': '20px', 'borderRadius': '5px','fontFamily': 'Raleway, sans-serif'}),
], style={'font-family': 'Raleway, sans-serif'})

# Define server for running in notebooks
server = app.server

# Callback to update the graph based on filters
@app.callback(
    Output('participation-timeline', 'figure'),
    [Input('season-filter', 'value'),
     Input('gender-filter', 'value'),
     Input('country-filter', 'value'),
     Input('sport-filter', 'value'),
     Input('medal-filter', 'value'),
     Input('year-range-slider', 'value')]
)
def update_timeline(season, gender, country, sport, medal, year_range):
    start_year, end_year = year_range

    # Filter data based on the selected filters
    df_filtered = athlete_events.copy()
    df_filtered = df_filtered[(df_filtered['Year'] >= start_year) & (df_filtered['Year'] <= end_year)]
    if season != 'All':
        df_filtered = df_filtered[df_filtered['Season'] == season]
    if gender != 'All':
        df_filtered = df_filtered[df_filtered['Sex'] == gender]
    if country != 'All':
        df_filtered = df_filtered[df_filtered['NOC'] == country]
    if sport != 'All':
        df_filtered = df_filtered[df_filtered['Sport'] == sport]
    if medal != 'All':
        if medal == 'None':
            df_filtered = df_filtered[pd.isnull(df_filtered['Medal'])]
        else:
            df_filtered = df_filtered[df_filtered['Medal'] == medal]

    # Aggregate data to get the number of participants per year
    filtered_timeline = df_filtered.groupby('Year')['ID'].nunique().reset_index(name='Number of Participants')

    # Update the figure
    fig = px.line(
        filtered_timeline,
        x="Year",
        y="Number of Participants",
        title='Olympics Participation Over the Years',
        color_discrete_sequence=['#003366'],  # Sets the line color to black
    )
    # Make the line thicker
    fig.update_traces(line=dict(width=2))  # Line made thicker

    fig.update_layout(
        title={
            'text': "<b>Olympics Participation Over the Years</b>",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'family': "Raleway, sans-serif",
                'size': 24,
                'color': '#2e4551'
            }
        },
        xaxis=dict(
            title_text="Year",
            title_font=dict(
                family="Raleway, sans-serif",
                size=18,
                color="#7f7f7f"
            )
        ),
        yaxis=dict(
            title_text="Number of Participants",
            title_font=dict(
                family="Raleway, sans-serif",
                size=18,
                color="#7f7f7f"
            )
        )
    )
    return fig

# Add to the callbacks
@app.callback(
    Output('top-athletes-chart', 'figure'),
    [Input('season-filter', 'value'),
     Input('gender-filter', 'value'),
     Input('country-filter', 'value'),
     Input('sport-filter', 'value'),
     Input('medal-filter', 'value'),
     Input('year-range-slider', 'value')]
)

def update_top_athletes_chart(season, gender, country, sport, medal, year_range):
    start_year, end_year = year_range

     # Filter data based on the selected filters
    df_filtered = athlete_events.copy()
    df_filtered = df_filtered[(df_filtered['Year'] >= start_year) & (df_filtered['Year'] <= end_year)]
    if season != 'All':
        df_filtered = df_filtered[df_filtered['Season'] == season]
    if gender != 'All':
        df_filtered = df_filtered[df_filtered['Sex'] == gender]
    if country != 'All':
        df_filtered = df_filtered[df_filtered['NOC'] == country]
    if sport != 'All':
        df_filtered = df_filtered[df_filtered['Sport'] == sport]
    if medal != 'All':
        if medal == 'None':
            df_filtered = df_filtered[pd.isnull(df_filtered['Medal'])]
        else:
            df_filtered = df_filtered[df_filtered['Medal'] == medal]
    # Count only rows where 'Medal' is not NA
    top_athletes = df_filtered[df_filtered['Medal'].notna()].groupby('Name')['Medal'].count().nlargest(10).reset_index()
    fig = px.bar(top_athletes, x='Name', y='Medal', title='Top 10 Athletes', color='Name',  color_discrete_sequence=['#003366'] * len(top_athletes))
    fig.update_layout(
        title={
            'text': "<b>Top 10 Athletes</b>",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'family': "Raleway, sans-serif",
                'size': 24,
                'color': '#2e4551'
            }
        },
        xaxis=dict(
            title_text="Name of Athlete",
            title_font=dict(
                family="Raleway, sans-serif",
                size=18,
                color="#7f7f7f"
            )
        ),
        yaxis=dict(
            title_text="# of Medals won",
            title_font=dict(
                family="Raleway, sans-serif",
                size=18,
                color="#7f7f7f"
            )
        )
    )
    fig.update_traces(marker=dict(color='#003366'), showlegend=False)  # Update marker color and hide legend
    return fig

@app.callback(
    Output('athlete-profile', 'data'),
    [Input('top-athletes-chart', 'hoverData')]
)


def update_athlete_profile(hoverData):
    if hoverData is None:
        return []
    athlete_name = hoverData['points'][0]['x']
    athlete_data = athlete_events[athlete_events['Name'] == athlete_name]
    athlete_data_with_medals = athlete_data.dropna(subset=['Medal'])  # Filter rows where 'Medal' is not NA
    max_year = athlete_data['Year'].max()  # Get the maximum year with a medal
    athlete_data_at_max_year = athlete_data[athlete_data['Year'] == max_year]  # Filter data for the maximum year
    profile = {
        'Name': athlete_name,
        'Nationality': athlete_data_at_max_year['NOC'].iloc[0],
        'Sex': athlete_data_at_max_year['Sex'].iloc[0],
        'Age (Latest)': athlete_data_at_max_year['Age'].mean(),
        'Height (Latest)': athlete_data_at_max_year['Height'].mean(),
        'Weight (Latest)': athlete_data_at_max_year['Weight'].mean(),
        'Sport': athlete_data_at_max_year['Sport'].iloc[0],
        'Year of First Medal': athlete_data_with_medals['Year'].min(),
        'Year of Last Medal': max_year
    }
    return [profile]


# Start the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)


# %%



