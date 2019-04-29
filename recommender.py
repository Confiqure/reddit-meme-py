calcs = ['Manhattan', 'Euclidean', 'Pearson', 'Cosine']


class Recommender:

    def __init__(self, input_data):
        """initialize recommender"""
        if type(input_data).__name__ == 'dict':
            self._data = input_data

    def compute_nearest_neighbor(self, username, r):
        """creates a sorted list of users based on their distance to username"""
        distances = []
        for instance in self._data:
            if instance != username:
                if r == 1 or r == 2:
                    distance = minkowski(self._data[username], self._data[instance], r)
                elif r == 3:
                    distance = pearson(self._data[username], self._data[instance])
                elif r == 4:
                    distance = cosine(self._data[username], self._data[instance])
                else:
                    distance = 0
                distances.append((instance, distance))
        # sort based on distance -- closest first
        if r == 1 or r == 2:
            distances.sort(key=lambda tup: tup[1])
        elif r == 3 or r == 4:
            distances.sort(key=lambda tup: tup[1], reverse=True)
        return distances

    def recommend(self, username, r):
        """Give list of recommendations"""
        # first find nearest neighbor
        nearest = self.compute_nearest_neighbor(username, r)[0][0]
        recs = []
        # now find bands neighbor rated that user didn't
        neighbor_ratings = self._data[nearest]
        user_ratings = self._data[username]
        for artist in neighbor_ratings:
            if artist not in user_ratings:
                recs.append((artist, neighbor_ratings[artist]))
        # using the fn sorted for variety - sort is more efficient
        # recommendations.sort(key=lambda artistTuple: artistTuple[1], reverse = True)
        return sorted(recs, key=lambda artist_tuple: artist_tuple[1], reverse=True)


def minkowski(rating1, rating2, r):
    """Computes the Minkowski distance.
    Both rating1 and rating2 are dictionaries
    for two users/entities"""
    distance = 0
    common_ratings = False
    for key in rating1:
        if key in rating2:
            distance += abs(rating1[key] - rating2[key]) ** r
            common_ratings = True
    if common_ratings:
        return distance ** (1 / r)
    else:
        return -1  # Indicates no ratings in common


def pearson(rating1, rating2):
    """Computes the Pearson coefficient.
    Both rating1 and rating2 are dictionaries
    for two users/entities"""
    x = list()
    y = list()
    for key in rating1:
        if key in rating2:
            x.append(rating1[key])
            y.append(rating2[key])
    n = len(x)
    if n == 0:
        return 0  # Indicates no ratings in common
    mx = sum(x) / float(n)
    my = sum(y) / float(n)
    r_num = 0
    r_den_x = 0
    r_den_y = 0
    for i in range(n):
        x_diff = x[i] - mx
        y_diff = y[i] - my
        r_num += x_diff * y_diff
        r_den_x += x_diff ** 2
        r_den_y += y_diff ** 2
    r_den = r_den_x ** 0.5 * r_den_y ** 0.5
    if r_den == 0:
        return 0
    r = r_num / r_den
    return r


def cosine(rating1, rating2):
    """Computes the cosine similarity.
    Both rating1 and rating2 are dictionaries
    for two users/entities"""
    x = list()
    y = list()
    for key in rating1:
        if key in rating2:
            x.append(rating1[key])
            y.append(rating2[key])
    n = len(x)
    if n == 0:
        return 0  # Indicates no ratings in common
    vector_x = 0
    vector_y = 0
    dot_product = 0
    for i in range(n):
        dot_product += x[i] * y[i]
        vector_x += x[i] ** 2
        vector_y += y[i] ** 2
    den = vector_x ** 0.5 * vector_y ** 0.5
    if den == 0:
        return 0
    return dot_product / den


def load_people():
    data = dict()
    with open('../People.csv', 'r') as file:
        content = file.readlines()
    content = [x.strip() for x in content]
    for person in content:
        name = person.split(',')[0]
        if name not in data:
            data[name] = dict()
    return dict(sorted(data.items()))


def load_movie_ratings(data):
    with open('../Ratings.csv', 'r') as file:
        content = file.readlines()
    content = [x.strip() for x in content]
    for rating in content:
        parts = rating.split(',')
        # parts[0] = movie name
        # parts[1] = person
        # parts[2] = rating
        if parts[1] in data:
            data[parts[1]][parts[0]] = float(parts[2])


def load_book_titles():
    data = dict()
    with open('../Books.csv', 'r') as file:
        content = file.readlines()
    content = [x.strip() for x in content]
    for rating in content:
        parts = rating.split(';')
        # parts[0] = ISBN
        # parts[1] = title
        data[parts[0]] = parts[1]
    return data


def load_book_ratings():
    data = dict()
    with open('../BookRatings.csv', 'r') as file:
        content = file.readlines()
    content = [x.strip() for x in content]
    for rating in content:
        parts = rating.split(';')
        # parts[0] = person
        # parts[1] = book
        # parts[2] = rating
        if parts[0] in data:
            data[parts[0]][parts[1]] = float(parts[2].replace(',', ''))
        else:
            data[parts[0]] = dict()
    return data


def recommend_movies():
    people = load_people()
    load_movie_ratings(people)
    rec = Recommender(people)
    while True:
        person = input('Enter Name: ')
        if person not in people:
            print('That person does not exist. Please try one of the following: %s' % ', '.join(people.keys()))
            continue

        for x in range(len(calcs)):
            neighbors = rec.compute_nearest_neighbor(person, x + 1)
            recommendations = rec.recommend(person, x + 1)
            print('%s Neighbors:' % calcs[x])
            for neighbor in neighbors:
                print('%s --> %.2f' % (neighbor[0], neighbor[1]))
            print('%s Recommendations:' % calcs[x])
            for recommendation in recommendations:
                print('%s --> %.2f' % (recommendation[0], recommendation[1]))
            print()


def recommend_books():
    titles = load_book_titles()
    people = load_book_ratings()
    rec = Recommender(people)
    while True:
        person = input('Enter Name: ')
        if person not in people:
            print('That person does not exist. Please try one of the following: %s' % ', '.join(people.keys()))
            continue

        for x in range(len(calcs)):
            recommendations = rec.recommend(person, x + 1)
            print('%s Recommendations:' % calcs[x])
            iterations = min(20, len(recommendations))
            for i in range(iterations):
                print('%s\t%s --> %.3f' % (recommendations[i][0], titles[recommendations[i][0]]
                                           if recommendations[i][0] in titles else 'Unknown Title',
                                           recommendations[i][1]))
            print()


if __name__ == "__main__":
    # recommend_movies()
    recommend_books()
