from dash import Dash, html, dcc, dash_table
from dash_bootstrap_templates import load_figure_template
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc  # MORPH, SLATE, MATERIA, SPACELAB, YETI, DARKLY

load_figure_template('DARKLY')

app = Dash('Spotify Tracks: Visual Analysis', external_stylesheets=[dbc.themes.DARKLY,
                                                                    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css'])
server = app.server

app.title = 'Spotify Tracks: Visual Analysis'

# df = pd.read_csv('https://...') #NEED TO UPLOAD CSV TO GITHUB

# READ FILE FROM FILE PATH
df = pd.read_csv('./data/SpotifyTracksDataset.csv')


def create_graph_page_1():
    # DISTINCT SONGS ONLY
    df = pd.read_csv('./data/SpotifyTracksDataset.csv')
    df = df.drop_duplicates(subset='track_name')

    # SORTING BY POPULARITY
    sorted_df = df.sort_values(by='popularity', ascending=False)

    # TO GET TOP 10 SONGS
    top_songs = sorted_df.head(10)

    # CREATING A BAR CHART
    fig = px.bar(top_songs, x='track_name', y='popularity',
                 # hover_name = 'track_name',
                 hover_data=['artists'],
                 color='track_genre',
                 color_discrete_sequence=px.colors.qualitative.Prism,
                 # title = 'Top 10 Most Popular Songs by Genre',
                 labels={'popularity': 'Song Popularity', 'track_name': 'Song Name'}, height=500)
    return dcc.Graph(figure=fig)


def create_graph_page_2():
    # FIND THE TOP 10 SONGS
    sorted_df = df.sort_values(by='popularity', ascending=False)

    # ENSURE UNIQUE SONGS
    top_songs = sorted_df.drop_duplicates(subset='track_name', keep='first')

    top_songs = top_songs.head(10)

    # FIND TEMPO OF EACH SONG
    tempos = top_songs['tempo'].tolist()

    # FIND AVG TEMPO
    total = sum(tempos)
    count = len(tempos)
    avg_tempo = total / count

    # PLOT TOP 10 MOST POPULAR SONGS
    fig = px.bar(top_songs, x='track_name', y='tempo',
                 hover_data=['artists'],
                 color='tempo',
                 color_continuous_scale='tempo',
                 text='tempo',
                 labels={'track_name': 'Song Name', 'tempo': 'Song Tempo'}, height=500)

    # PLOT AVG TEMPO LINE
    fig.add_hline(y=avg_tempo,
                  line_width=2,
                  line_color='red',
                  annotation_text=f'Average Tempo = {avg_tempo: .2f}',
                  annotation_position='top left')

    return dcc.Graph(figure=fig)


def create_graph_page_3():
    # FILTER AND FIND PERCENTAGES
    count_maj_explicit = df[(df['mode'] == 1) & (df['explicit'] == True)].shape[0]
    count_maj_total = df[df['mode'] == 1].shape[0]
    percentage_maj_explicit = count_maj_explicit / count_maj_total * 100

    count_min_explicit = df[(df['mode'] == 0) & (df['explicit'] == True)].shape[0]
    count_min_total = df[df['mode'] == 0].shape[0]
    percentage_min_explicit = count_min_explicit / count_min_total * 100

    # NEW DF FOR THE PIE CHART
    pie_data = pd.DataFrame({'mode': ['Major', 'Minor']
                                , 'percentage': [percentage_maj_explicit, percentage_min_explicit]})

    # CREATING A PIE CHART
    fig = px.pie(pie_data,
                 values='percentage',
                 names='mode',
                 color='mode',
                 color_discrete_sequence=px.colors.qualitative.Prism,
                 # title = 'Percentage of Explicit Songs by Mode',
                 height=500)
    fig.update_traces(textfont_size=20)

    return dcc.Graph(figure=fig)


def create_graph_page_4():
    # DISTINCT SONGS ONLY
    df = pd.read_csv('./data/SpotifyTracksDataset.csv')
    df = df.drop_duplicates(subset='track_name')

    # SORTING BY POPULARITY
    sorted_df = df.sort_values(by='popularity', ascending=False)

    # TO GET TOP 10 SONGS
    top_songs = sorted_df.head(10)

    # TO SORT THE BAR CHART BY VALENCE
    sort_by_valence = top_songs.sort_values(by='valence', ascending=False)

    # CREATING A BAR CHART
    fig = px.bar(sort_by_valence, x='track_name', y='valence',
                 hover_data=['artists', 'valence'],
                 color='valence',
                 color_continuous_scale='tempo',
                 # title = 'Top 10 Most Popular Songs by Valence',
                 labels={'valence': 'Song Positivity', 'track_name': 'Song Name'}, height=500)

    return dcc.Graph(figure=fig)


def create_graph_page_5a():
    # TO COUNT EACH OCCURENCE OF ALL TIME SIGNATURES
    time_sig_count = df['time_signature'].value_counts().reset_index()
    time_sig_count.columns = ['time_signature', 'count']

    # CREATING A PIE CHART
    fig = px.pie(time_sig_count,
                 values='count',
                 names='time_signature',
                 color='time_signature',
                 color_discrete_sequence=px.colors.qualitative.Prism,
                 title='Frequency of Time Signatures',
                 height=500)
    fig.update_traces(textfont_size=20)

    return dcc.Graph(figure=fig)


def create_graph_page_5b():
    # CATEGORIZING SONGS BY METER
    df['meter'] = df['time_signature'].apply(lambda x: 'Even Meter' if x == 4 else 'Odd Meter')

    # CALCULATING POPULARITY BY METER
    meter_pop = df.groupby('meter')['popularity'].sum().reset_index()

    # CREATING A BAR CHART
    fig = px.bar(meter_pop, x='meter', y='popularity',
                 hover_data=['popularity'],
                 color='meter',
                 color_discrete_sequence=px.colors.qualitative.Prism,
                 title='Total Popularity by Meter Category',
                 labels={'meter': 'Meter', 'popularity': 'Sum of Popularity'}, height=500)

    return dcc.Graph(figure=fig)


def create_graph_page_6():
    # CONVERTING SONG DURATION TO MINUTES
    df['duration_min'] = df['duration_ms'] / 60000

    # GROUPING BY GENRE AND CALCULATING AVG SONG LENGTH
    avg_length = df.groupby('track_genre')['duration_min'].mean().reset_index()

    # SORT BY AVG LENGTH
    top10 = avg_length.sort_values(by='duration_min', ascending=False).head(10)

    # CREATING A BAR CHART
    fig = px.bar(top10, x='track_genre', y='duration_min',
                 hover_data=['track_genre', 'duration_min'],
                 color='track_genre',
                 color_discrete_sequence=px.colors.qualitative.Prism,
                 title='Top 10 Genres with Longest Average Song Length',
                 labels={'track_genre': 'Song Genre', 'duration_min': 'Average Song Duration (in minutes)'}, height=500)

    return dcc.Graph(figure=fig)


def spotify_tracks_data():
    return dash_table.DataTable(
        data=df.head().to_dict('records'),
        columns=[{'name': i, 'id': i} for i in df.columns],
        style_data={
            'backgroundColor': 'rgb(51, 89, 122)',
            'color': 'white',
            'height': '50px'
        },
        style_header={
            'backgroundColor': 'rgb(11, 49, 82)',
            'fontWeight': 'bold'
        },
        style_table={
            'height': '300px',
            'overflowY': 'auto'
        },
    )


home_page_layout = dbc.Container([
    # CREATING THE NAVBAR
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink(html.I(className='fab fa-github'),
                                    href='https://github.com/BenSolomon27', target='_blank')),
        ],
        brand=dbc.Col(html.Img(src='https://images.plot.ly/logo/new-branding/plotly-logomark.png',
                               height='30px')),
        brand_href='#',
        color='muted',
        dark=True,
    ),
    # PROJECT HEADER PLAIN
    dbc.Row([
        dbc.Col([
            html.H1('Spotify Tracks: Visual Analysis', className='text-decoration-underline',
                    style={'textAlign': 'center', 'fontWeight': 'bold'})
        ], width=12, className='mt-3')
    ]),
    # PROJECT INTRODUCTION
    dbc.Row([
        dbc.Col([
            dbc.Card(
                [
                    html.H5('''Hi, my name is Ben Solomon - welcome to my first Dash App! This app aims to demonstrate
                    some analyses I have conducted using a Spotify Tracks dataset. Each page of this app covers
                    a central question I had regarding elements within the dataset. Much of this data is used by Spotify
                    in their song recommendation algorithm, so I thought it could be interesting to take a deeper 
                    look into some of the relationships between these elements. I hope you learn something new 
                    from taking a look at these graphs! To best understand these visuals, below is a table
                    displaying the first five rows of data.''')
                ],
                body=True,
                color='dark'
            )
        ], width=12, className='mt-3')
    ]),
    # VIEWING THE DATASET
    dbc.Row([
        dbc.Col([
            dbc.Card(
                [html.H3('''The Dataset:''', className='text-decoration-underline'),
                 spotify_tracks_data()],
                body=True,
                color='dark'
            )
        ], width=12, className='mt-3')
    ]),
])

page_1_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2('Question 1: What genres are the top 10 most popular songs?')
        ], width=12, className='mt-3')
    ]),
    dbc.Row([
        dbc.Col([
            html.H5('''If you are in the US like myself, 
            my guess is that most of you would argue that the most popular genre of music at the moment is pop.
            However, this dataset contains international streaming data, so the results might surprise you.''',
                    className='text-muted')
        ], width=12, className='mt-3')
    ]),
    create_graph_page_1(),
    html.H5('''Looks like people overwhelmingly enjoy Latin music above all else,
    which makes sense considering Spanish is the second most spoken native language. 
    Bad Bunny is doing pretty well, making up half of the top 10 songs!''', className='text-muted mt-3')
])

page_2_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2('Question 2: What is the average tempo for the top 10 most popular songs?')
        ], width=12, className='mt-3')
    ]),
    dbc.Row([
        dbc.Col([
            html.H5('''As a practicing musician, I often hear industry professionals say that a modern 
            hit song lies within a certain tempo range. Let's see if the data backs this up!''',
                    className='text-muted')
        ], width=12, className='mt-3')
    ]),
    create_graph_page_2(),
    html.H5('''Seems like that hit song tempo is about 113 BPM - checks out to me!''',
            className='text-muted mt-3')
])

page_3_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2('Question 3: Is there a relationship between explicit songs and their mode?')
        ], width=12, className='mt-3')
    ]),
    dbc.Row([
        dbc.Col([
            html.H5('''My motivation behind this question stems from my curiosity about the impact of 
            tonality on listeners. People often consider minor songs to be more sad or negative, 
            so I wondered whether this translated to songs being more explicit as well...''',
                    className='text-muted')
        ], width=12, className='mt-3')
    ]),
    create_graph_page_3(),
    html.H5('''Unsurprisingly, more explicit songs are in minor keys than major. 
    However, there is less of a difference here than I imagined there would be, 
    as only about 10% more explicit songs are in minor keys than major keys. ''',
            className='text-muted mt-3')
])

page_4_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2('Question 4: How are Popularity and Valence Related?')
        ], width=12, className='mt-3')
    ]),
    dbc.Row([
        dbc.Col([
            html.H5('''This question is somewhat of an extension to the previous question. However, we will now 
            focus on whether a song's positivity impacts its popularity. To examine this question, we'll need to 
            take a few things into consideration. First, in the interest of maintaining visual clarity, we will 
            look at the top 10 most popular songs. Also, valence is measured from a range of 0 to 1, with one 
            being the most positive. How positive would you guess the 10 most popular songs are?''',
                    className='text-muted')
        ], width=12, className='mt-3')
    ]),
    create_graph_page_4(),
    html.H5('''Looks like over half of the 10 most popular songs are on the more negative side. 
    Pretty surprising to me! ''',
            className='text-muted mt-3')
])

page_5_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2('Question 5: What are the least popular time signatures?')
        ], width=12, className='mt-3')
    ]),
    dbc.Row([
        dbc.Col([
            html.H5('''You might know that a large majority of pop music is in 4/4. 
            However, as a fan of progressive metal and jazz, I love music in odd meter. Given this dataset 
            contains data about time signature, I was curious to see what the least popular time signatures are. 
            We will look at two things here: (1) Frequency of use of all time signatures in the data and (2) 
            Popularity of songs based on their meter. This begs the question, does a song being in odd meter 
            make it less popular? ''',
                    className='text-muted')
        ], width=12, className='mt-3')
    ]),
    create_graph_page_5a(),
    create_graph_page_5b(),
    html.H5('''Almost 90% of songs from this dataset are in 4/4! This will bias the data in the bar chart, however. 
    We see that even meter songs (for this dataset, that's any song that's not in 4) are much more popular. 
    You could also argue that the reason so many songs in this dataset are in 4/4 in the first place is because 
    they are inherently more popular.''',
            className='text-muted mt-3')
])

page_6_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2('Question 6: Which genres have the longest average song length?')
        ], width=12, className='mt-3')
    ]),
    dbc.Row([
        dbc.Col([
            html.H5('''Similar in concept to tempo, a modern hit song lies within a certain range. 
            In this case, I'd imagine that's somewhere between 2 to 3 minutes. If I had to guess, I'd say pop 
            songs likely have the shortest average song length. Instead, let's look at the top 10 genres with the 
            longest average song length. Which genre do you think will have the longest song length?''',
                    className='text-muted')
        ], width=12, className='mt-3')
    ]),
    create_graph_page_6(),
    html.H5(''' Had a feeling I'd find metal somewhere in this list! Considering these are not your typical 
    radio-friendly genres, it's not too surprising to see these as having the longest average song lengths. This 
    observation supports the idea that hit songs lie within a certain range - all of these genres have an average 
    song length well over 3 minutes!''',
            className='text-muted mt-3')
])


def render_page_content(page):
    if page == '/':
        return home_page_layout
    elif page == '/page-1':
        return page_1_layout
    elif page == '/page-2':
        return page_2_layout
    elif page == '/page-3':
        return page_3_layout
    elif page == '/page-4':
        return page_4_layout
    elif page == '/page-5':
        return page_5_layout
    elif page == '/page-6':
        return page_6_layout


sidebar_style = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20rem',
    'padding': '2rem 1rem',
    'background-color': '#393939',
}

content_style = {
    'margin-left': '17rem',
    'margin-right': '1rem',
    'padding': '2rem 1rem',
}

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            dbc.Nav(
                [
                    dbc.NavLink('Home', href='/', active='exact'),
                    dbc.NavLink('What genres are the top 10 most popular songs?', href='/page-1', active='exact'),
                    dbc.NavLink('What is the average tempo for the top 10 most popular songs?', href='/page-2',
                                active='exact'),
                    dbc.NavLink('Is there a relationship between explicit songs and their mode?', href='/page-3',
                                active='exact'),
                    dbc.NavLink('How are Popularity and Valence Related?', href='/page-4', active='exact'),
                    dbc.NavLink('What are the least popular time signatures?', href='/page-5', active='exact'),
                    dbc.NavLink('Which genres have the longest average song length?', href='/page-6', active='exact'),
                ],
                vertical=True,
                pills=True,
            ),
            style=sidebar_style
        ),
        dbc.Col(dcc.Location(id='url', refresh=False), width=10),
        dbc.Col(html.Div(id='page-content'), style=content_style, width=10),
    ]),
])


@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return home_page_layout
    elif pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    elif pathname == '/page-3':
        return page_3_layout
    elif pathname == '/page-4':
        return page_4_layout
    elif pathname == '/page-5':
        return page_5_layout
    elif pathname == '/page-6':
        return page_6_layout
    else:
        return html.Div(
            [
                html.H1('404: Not found', className='text-danger'),
                html.Hr(),
                html.P(f'The pathname {pathname} was not recognized...'),
            ],
            className='p-3 bg-light rounded-3',
        )


if __name__ == '__main__':
    app.run(debug=True)
    app.run(jupyter_mode='tab')
    # app.run(jupyter_mode = 'jupyterlab')