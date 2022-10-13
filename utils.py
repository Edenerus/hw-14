import sqlite3


def db_connect(path='netflix.db'):
    """
    Подключаемся к необходимой базе данных
    """
    con = sqlite3.connect(path)
    cur = con.cursor()
    return cur


def get_movie_by_title(title):
    """
    Возвращает фильм по названию
    """
    connect = db_connect()
    connect.execute(f"""
                    SELECT title, country, release_year,
                    listed_in, description
                    FROM netflix
                    WHERE title LIKE '%{title}%'
                    ORDER BY release_year DESC
                    LIMIT 1
                """)
    result = connect.fetchone()
    return {
        "title": result[0],
        "country": result[1],
        "release_year": result[2],
        "genre": result[3],
        "description": result[4]
    }


def get_movie_by_year(one_year, two_year):
    """
    Возвращает список фильмов по годам
    """
    connect = db_connect()
    connect.execute(f"""
                    SELECT title, release_year
                    FROM netflix
                    WHERE release_year
                    BETWEEN {one_year} AND {two_year}
                    LIMIT 100
                    """)
    result = connect.fetchall()
    result_list = []
    for title in result:
        result_list.append({'title': title[0],
                            'release_year': title[1]})
    return result_list


def get_movie_by_rating(rating):
    """
    Возвращает список фильмов по рейтингу
    """
    connect = db_connect()
    rating_parameter = {
        "children": "'G'",
        "family": "'G', 'PG', 'PG-13'",
        "adult": "'R', 'NC-17'"
    }
    if rating not in rating_parameter:
        return "Такого рейтинга нет"
    connect.execute(f"""
                    SELECT title, rating, description
                    FROM netflix
                    WHERE rating IN ({rating_parameter[rating]})
                    LIMIT 100
                    """)
    result = connect.fetchall()
    result_list = []
    for title in result:
        result_list.append([{"title": title[0],
                             "rating": title[1],
                             "description": title[2]}])
    return result_list


def get_movie_by_genre(genre):
    """
    Возвращает список фильмов по жанру
    """
    connect = db_connect()
    connect.execute(f"""
                    SELECT title, description
                    FROM netflix
                    WHERE listed_in LIKE '%{genre}%'
                    ORDER BY release_year DESC 
                    LIMIT 10
                    """)
    result = connect.fetchall()
    result_list = []
    for title in result:
        result_list.append([{"title": title[0],
                             "description": title[1]}])
    return result_list


def get_movie_by_actor(actor_one, actor_two):
    """
    Возвращает список актеров, которые играли более двух раз
    с актерами, переданными в аргумент функции
    """
    connect = db_connect()
    connect.execute(f"""SELECT netflix.cast 
                    FROM netflix 
                    WHERE netflix.cast LIKE '%{actor_one}%'
                    AND netflix.cast LIKE '%{actor_two}%'""")
    result = connect.fetchall()
    actors_list = []
    for cast in result:
        actors_list.extend(cast[0].split(', '))
    result_actors = []
    for a in actors_list:
        if a not in [actor_one, actor_two]:
            if actors_list.count(a) > 2:
                result_actors.append(a)
    return set(result_actors)


def get_movie(type_film, release_year, genre):
    """
    Возвращает фильм по заданным параметрам
    """
    connect = db_connect()
    connect.execute(f"""
                      SELECT title, description
                      FROM netflix
                      WHERE `type` = '{type_film}'
                      AND release_year = {release_year}
                      AND listed_in LIKE '%{genre}%'
                        """)
    results = connect.fetchall()
    result_json = []
    for result in results:
        result_json.append({
            'title': result[0],
            'description': result[1],
            })
    return result_json
