import os
import random
import json

LINE_LENGTH = 30
CONSTANT = 10

data = []

with open("movies.data", 'r') as f:
    content = f.read()
    if len(content) != 0:
        data = json.loads(content)

def save():
    with open("movies.data", "w+") as f:
        f.write(json.dumps(data))

def clear():
    os.system("clear")

def _input(output, type_cast):
    invalid = 0
    while(1):
        print(' ' * LINE_LENGTH * 3, end='\r')
        if len(_in := input(output)):
            try:
                _in = type_cast(_in)
                return _in
            except:
                invalid = 1
                print("Invalid type")
                print("\033[F", end='')
        if invalid == 2:
            print(' ' * LINE_LENGTH, end='\r')
            invalid = False
        elif invalid:
            invalid = 2
        print("\033[F", end='')

def get_random_movie():
    return data[random.randint(0, len(data) - 1)]

def get_n_random_movies(n, movies=[]):
    if n > len(data):
        return data
    
    return random.sample(data, n)


def compare_2_movies(movie1, movie2):
    print(f"1. {movie1['name']}")
    print(f"2. {movie2['name']}")
    choice = _input("1 or 2: ", int)

    m1_rating = movie1["score"]
    m2_rating = movie2["score"]

    p1 = 1 / (1 + pow(10, (m1_rating - m2_rating) / 100))
    p2 = 1 / (1 + pow(10, (m2_rating - m1_rating) / 100))

    p1_a = 1 if choice == 1 else 0
    p2_a = not p1_a

    movie1["score"] += (10 * CONSTANT * (p1_a - p1)) // 10
    movie2["score"] += (10 * CONSTANT * (p2_a - p2)) // 10

def new_movie():
    clear()
    name = _input("Name: ", str)
    data.append({"name": name, "score": 50})
    choice = input(f"Would you like to compare {name}? y/N: ")

    if len(choice) and choice[0].lower() != 'y':  # yes
        movie = data[-1]
        movies = get_n_random_movies(5, [movie])
        for other_movie in movies:
            compare_2_movies(movie, other_movie)


def compare_movies():
    while 1:
        clear()
        movies = get_n_random_movies(2)
        compare_2_movies(movies[0], movies[1])
        
        stop = input("Continue Y/n: ")
        if len(stop) and stop[0] == 'n':
            break

def list_movies():
    clear()

    movies = sorted(data, key=lambda movie: -movie['score'])[0:50]
    for i, movie in enumerate(movies):
        print(f"{i+1}. ({movie['score']}) - {movie['name']}")

    input("Press any key to continue...")

def menu():
    while 1:
        print(".: Movie Rating :.".center(LINE_LENGTH))
        print('=' * LINE_LENGTH)
        print("1: Add new movie")
        print("2: Compare movies")
        print("3: Search for a movie")
        print("4: List movies")
        print("5: Exit")
        choice = _input("Choice: ", int)
        match choice:
            case 1:
                new_movie()
            case 2:
                compare_movies()
            case 3:
                search()
            case 4:
                list_movies()
            case 5:
                save()
                exit(0)
        
        clear()

try:
    menu()
except:
    save()