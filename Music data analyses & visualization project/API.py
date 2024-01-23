from xml.sax import parseString
import re
from bs4 import BeautifulSoup
import requests
import os
import sqlite3
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

def authentication():

    AUTH_URL = 'https://accounts.spotify.com/api/token'

    # POST
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': "f625e8875cad4052bc9e29872bd62523",
        'client_secret': "c145b321c26b42e1871b412a8eeb48e7",
        })

    # convert the response to JSON
    auth_response_data = auth_response.json()

    # save the access token
    access_token = auth_response_data['access_token']
    return access_token

def get_artist_info(access_token, ID):

    headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}

    BASE_URL = 'https://api.spotify.com/v1/artists/'

    #ID = "0TnOYISbd1XYRBk9myaseg"
    #ID2 = "00FQb4jTyendYWaN8pK0wa"

    #Create a list and go through the list
    r = requests.get(BASE_URL + ID , headers=headers)
    r = r.text
    r = json.loads(r)
    name = r["name"]
    popularity = r["popularity"]
    genres = r["genres"]
    return (ID, name, genres, popularity)
    
uri_list = [
    '4q3ewBCX7sLwd24euuV69X', #bad bunny
    '06HL4z0CvFAxyc27GXpf02', #taylor swift
    '6KImCVD70vtIoJWnq6nGn3', #harry styles
    '3TVXtAsR1Inumwj472S9r4', #drake
    '4oUHIQIBe0LHzYfvXNW4QM', #morgan wallen
    '5cj0lLjcoR7YOSnhnX0Po5', #doja cat
    '6eUKZXaKkcviH0Ku9w2n3V', #ed sheeran
    '4dpARuHxo51G3z768sgnrY', #adele
    '1Xyo4u8uXC1ZmMpatF05PJ', #the weeknd
    '5f7VJjfbwm532GiveGC0ZK', #lil baby
    '1RyvyyTE3xzB2ZywiAwp0i', #future
    '1uNFoZAHBGtllmzznpCI3s', #justin bieber
    '246dkjvS1zLTtiykXe5h60', #post malone
    '2LIk90788K0zvyj2JJVwkJ', #jack harlow
    '2YZyLoL8N0Wb9xBt1NhZWg', #kendrick lamar
    '718COspgdWOnwOFpJHRZHS', #luke combs
    '4MCBfE4596Uoi2O4DtmEMz', #juice wrld
    '4yvcSjfu4PC0CYQyLy4wSq', #glass animals
    '3hcs9uc56yIGFCSy9leWe7', #lil durk
    '7jVv8c5Fj3E9VhNjxT4snq', #lil nas x
    '6M2wZ9GZgrQXHCFfjv46we', #dua lipa
    '3PhoLpVuITZKcymswpck5b', #elton john
    '7wlFDEWiM5OoIAt8RSli8b', #youngboy never broke again
    '45TgXXqMDdF8BkjA83OM7z', #rod wave
    '5K4W6rqBFWDnAN6FQUkS6x', #kanye west
    '1McMsnEElThX1knmY4oliG', #olivia rodrigo
    '6vWDO969PvNqNYHIOW5v0m', #beyonce
    '2tIP7SsRs7vjIcLrU85W8J', #the kid laroi
    '6qqNVTkY8uBg9cP3Jd7DAH', #billie eilish
    '46SHBwWsqBkxI7EeeBEQG7', #kodak black
    '56oDRnqbIiwx4mymNEv7dS', #lizzo
    '2hlmm7s2ICUX0LVIhVFlZQ', #gunna
    '53XhwfbYqKCa1cC15pYq2q', #imagine dragons
    '3MdXrJWsbVzdn6fe5JYkSQ', #latto
    '4YLtscXsxbVgi031ovDDdh', #chris stapleton
    '57LYzLEk2LcFghVwuWbcuS', #summer walker
    '7sKxqpSqbIzphAKAhrqvlf', #walker hayes
    '6AgTAQt8XS6jRWi4sX7w49', #polo g
    '7tYKF4w9nC0nq9CsPZTHyP', #sza
    '0du5cEVh5yTK9QJze8zA0C', #bruno mars
    '40ZNYROS4zLfyyBSs2PGe2', #zach bryan
    '57vWImR43h4CaDao012Ofp', #steve lacy
    '7dGJo4pcD2V6oG8kP0tJRR', #eminem
    '3win9vGIxFfBRag9S63wwf', #bailey zimmerman
    '4V8LLVI7PbaPR0K2TGSxFF', #tyler, the creator
    '1aSxMhuvixZ8h9dK9jIDwL', #kate bush
    '790FomKkXshlbRYZFtlgla', #karol g
    '3oSJ7TBVCWMDMiYjXNiCKE', #kane brown
    '2VSHKHBTiXWplO8lxcnUC9', #gayle
    '0Njy6yR9LykNKYg9yE23QN', #nardo wick
    '1mfDfLsMxYcOOZkzBxvSVW', #cole swindell
    '66CXWjxzNUsdJxJ2JdwvnR', #ariana grande
    '4O15NlyKLIASxsJ0PrXPfz', #lil uzi vert
    '3Nrfpe0tUJi4K4DXYWgMUX', #bts
    '6zLBxLdl60ekBLpawtT63I', #cody johnson
    '6l3HvQ5sa6mXTsMTB19rO5', #j. cole
    '181bsRPaVXVlUKXrxwZfHK', #megan thee stallion
    '0hCNtLu0JehylgoiP8L4Gh', #nicki minaj
    '7bXgB6jMjp9ATFy66eO08Z', #chris brown
    '15UsOTVnJzReFVN1VCnxy4', #xxxtentacion
    '3jK9MiCrA42lLAdMGUZpwa', #anderson .paak
    '6TIYQ3jFPwQSRmorSezPxX', #machine gun kelly
    '0eDvMgVFoNV3TpwtrVCoTj', #pop smoke
    '3WrFJ7ztbogyGnTHbHJFl2', #the beatles
    '3tJoFztHeIJkJWMrx0td2f', #moneybagg yo
    '08GQAI4eElDnROBrJRGE0X', #fleetwood mac
    '1dfeR4HaWDbWqFHLkxsg1d', #queen
    '3FfvYsEGaIb52QPXhg4DcH', #jason aldean
    '7o2ZQYM7nTsaVdkXY38UAA', #em beihold
    '3fMbdgg4jU18AjLCKBhRSm', #michael jackson
    '5Pwc4xIPtQLFEnJriah9YJ', #onerepublic
    '0Y5tJX1MQlPlqiwlOH1tJY', #travis scott
    '699OTQXzgjhIYAHMy9RyPD', #playboi carti
    '4fxd5Ee7UefO4CUXgwJ7IP', #giveon
    '4iHNK0tOyZPYnBU7nGAgpQ', #mariah carey
    '1HY2Jd0NmPuamShAr6KMms', #lady gaga
    '2h93pZq0e7k5yf4dywlkpM', #frank ocean
    '3qiHUAX7zY4Qnjx8TNUzVx', #yeat
    '0L8ExT028jH3ddEcZwqJJ5', #red hot chili peppers
    '4sj6D0zlMOl25nprDJBiU9', #andy williams
    '77kULmXAQ6vWer7IIHdGzI', #jordan davis
    '0QHgL1lAIqAw0HtD7YldmP', #dj khaled
    '6U3ybJ9UHNKEdsH7ktGBZ7', #j.i.d
    '3qm84nBOXUEQ2vnTfUTTFC', #guns n’ roses
    '3MZsBdqDrRTJihTHQrO6Dq', #joji
    '6VuMaDnrHyPL1p4EHjYLi7', #charlie puth
    '1GxkXlMwML1oSg5eLPiAz3', #michael bublé
    '4xFUf1FHVy696Q1JQZMTRj', #carrie underwood
    '2ye2Wgw4gimLv2eAKyk1NB', #metallica
    '2W8yFh0Ga6Yf3jiayVxwkE', #dove cameron
    '5PYToRCsrnvikZg3yl2JMr', #stephanie beatriz
    '5SXuuuRpukkTvsLuUknva1', #baby keem
    '1mcTU81TzQhprhouKaTkpq', #rauw alejandro
    '3tlXnStJ1fFhdScmQeLpuG', #brent faiyaz
    '4vdAAzZBUKbsrvHi6UR7B7', #jessica darrow
    '37230BxxYs9ksS7OkZw3IU', #chenco corleone
    '4gzpq5DPGxSnKTe4SA8HAU', #coldplay
    '048LktY5zMnakWq7PTtFrz', #ckay
    '6olE6TJLqED3rqDCT0FyPh', #nirvana
    '1URnnhqYAYcrqrcwql10ft', #21 savage
]
#database

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def spotify_table1(artist_list, cur, conn):
    cur.execute('DROP TABLE IF EXISTS Genre_Info')
    cur.execute('CREATE TABLE Genre_Info (id INTEGER PRIMARY KEY NOT NULL, genres TEXT, genres_num INTEGER)')
    count = 1
    for tuple in artist_list:
        if len(str(tuple[2])) > 2:
            genres_num = str(tuple[2]).count(",") + 1
        else:
            genres_num = 0
        cur.execute("INSERT INTO Genre_Info (id, genres, genres_num) VALUES (?,?,?)", (count, str(tuple[2]), genres_num))
        count += 1
    conn.commit()
    cur.execute("SELECT id, genres, genres_num FROM Genre_Info ")
    for row in cur:
        print(row)
    cur.close
    

def spotify_table2(artist_list, cur, conn):
    sorted_artist_list = sorted(artist_list, key=lambda x:x[3], reverse=True)
    cur.execute('DROP TABLE IF EXISTS Popularity_Info')
    cur.execute('CREATE TABLE Popularity_Info (id INTEGER PRIMARY KEY NOT NULL, popularity INTEGER, spotify_rank INTEGER)')
    count = 1
    for tuple in artist_list:
        cur.execute("INSERT INTO Popularity_Info (id, popularity, spotify_rank) VALUES (?,?,?)", (count, int(tuple[3]), (sorted_artist_list.index(tuple) + 1)))
        count += 1
    conn.commit()
    cur.execute("SELECT id, popularity, spotify_rank FROM Popularity_Info ")
    for row in cur:
        print(row)
    cur.close

def billboard_table(link, cur, conn):
#   Creating the database from urls with
#   categories such as city name, median household income level, racial demographics of the area,
#   income change over time(?)
    resp = requests.get(link)
    soup = BeautifulSoup(resp.content, 'html.parser')
    n_list = []
    r_list = []
    tag = soup.find(class_="chart-results-list // u-padding-b-250")
    name_list = tag.find_all('h3')
    for item in name_list:
        name = item.text
        n_list.append(name.strip('\n\t'))
    rank_list = tag.find_all('span')
    for item in rank_list:
        rank = item.text
        r_list.append(rank.strip('\n\t'))
    tup_list = []
    for i in range(1, 101):
        tup = (i, n_list[i - 1], r_list[i - 1])
        tup_list.append(tup)
    cur.execute("DROP TABLE IF EXISTS BillBoard_Charts")
    cur.execute("CREATE TABLE BillBoard_Charts (id INTEGER PRIMARY KEY NOT NULL, name TEXT , rank INTEGER)")
    for item in tup_list:
        cur.execute("INSERT INTO BillBoard_Charts (id, name, rank) VALUES (?, ?, ?)", item)
    conn.commit()

    #print out database
    cur.execute("SELECT id, name, rank FROM BillBoard_Charts")
    for row in cur:
        print(row)
    cur.close
#the average number of genres
#the average ranking for each artist this should use join
def get_genre_average(cur, conn):
    total = 0
    cur.execute("SELECT genres FROM Genre_Info")
    for genre in cur:
        if len(genre) != 0:
            genre = str(genre)
            genre_num = genre.count(',') + 1
            total += genre_num
    return total / 100

def get_rank_averages(cur, conn):
    diff_dict = {}
    cur.execute('SELECT BillBoard_Charts.name, BillBoard_Charts.rank, Popularity_Info.spotify_rank FROM BillBoard_Charts JOIN Popularity_Info ON BillBoard_Charts.id = Popularity_Info.id')
    for row in cur:
        diff_dict[row[0]] = ((row[1] + row[2]) / 2)
    conn.commit()
    return diff_dict

def write_averages(avg_genre_num, diff_dict, file):
    fout = open(file, 'w')
    fout.write('Average ranks of each artist based on billboard and spotify data:\n')
    for item in diff_dict:
        fout.write(item + ': ' + str(diff_dict[item]) + '\n')
    fout.write('\nAverage number of genres of all artists\' discographies: ' + str(avg_genre_num))
    fout.close()

def graph_ranks(cur, conn):
    spotify_ranks = []
    billboard_ranks = []
    average_ranks = get_rank_averages(cur, conn)
    cur.execute('SELECT spotify_rank FROM Popularity_Info')
    for row in cur:
        spotify_ranks.append(row[0])
    cur.execute('SELECT rank FROM BillBoard_Charts')
    for row in cur:
        billboard_ranks.append(row[0])
    fig, ax = plt.subplots()
    ax.scatter(average_ranks.keys(), billboard_ranks, label='BillBoard Chart Rankings')
    ax.scatter(average_ranks.keys(), spotify_ranks, label='Spotify Chart Rankings')
    ax.scatter(average_ranks.keys(), average_ranks.values(), label='Average Chart Rankings')
    ax.legend()
    ticks_loc = list(ax.get_xticks())
    ax.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
    ax.set_xticklabels(average_ranks.keys(), rotation='vertical')
    ax.margins(0)
    ax.set_xlabel('Artist names')
    ax.set_ylabel('Chart placements')
    ax.set_title('Placements of BillBoard\'s 2022 Top 100 Artists on Spotify\'s Popularity Rankings')
    ax.grid()
    plt.show()

def genre_percentage(cur, conn):
    one_genre = 0
    two_genre = 0
    three_genre = 0
    four_or_more = 0
    unknown = 0
    cur.execute("SELECT genres_num FROM Genre_Info")
    for num in cur:
        num = int(num[0])
        if num == 1:
            one_genre += 1
        elif num == 2:
            two_genre += 1
        elif num == 3:
            three_genre += 1
        elif num >= 4:
            four_or_more += 1
        else:
            unknown += 1
    colors = ["gold", "yellowgreen", "lightcoral", "lightskyblue","grey"]
    percentages = [one_genre/100, two_genre/100, three_genre/100, four_or_more / 100, unknown / 100]
    lables = ["1 genre", "2 genres", "3 genres", "4 or more", "unknown" ]
    plt.pie(percentages, labels = lables, colors = colors, shadow= True,startangle=140, autopct='%.2f%%')
    plt.title("Number of Genres")
    plt.show()
if __name__ == '__main__':
    token = authentication()
    artist_list = []
    for id in uri_list[0:21]:
        artist_info = get_artist_info(token, id)
        artist_list.append(artist_info)
    
    for id in uri_list[21:41]:
        artist_info = get_artist_info(token, id)
        artist_list.append(artist_info)

    for id in uri_list[41:61]:
        artist_info = get_artist_info(token, id)
        artist_list.append(artist_info)
    
    for id in uri_list[61:81]:
        artist_info = get_artist_info(token, id)
        artist_list.append(artist_info)    

    for id in uri_list[81:]:
        artist_info = get_artist_info(token, id)
        artist_list.append(artist_info)

    cur, conn = open_database("project.db")
    spotify_table1(artist_list, cur, conn)
    spotify_table2(artist_list, cur, conn)

    cur, conn = open_database('project.db')
    #billboard_table('https://www.billboard.com/charts/year-end/top-artists/', cur, conn)
    
    rank_avgs = get_rank_averages(cur, conn)
    genre_avgs = get_genre_average(cur, conn)
    write_averages(genre_avgs, rank_avgs, 'output.txt')
    graph_ranks(cur, conn)
    genre_percentage(cur, conn)

