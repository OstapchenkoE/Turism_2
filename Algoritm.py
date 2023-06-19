import osmnx as ox
import networkx as nx
# import pandas as pd
import folium
from math import sin, cos, sqrt, atan2, radians
import random
import time
import sys


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6373.0
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


from eternity import russia_map, df_cut

# from app import kol,name
# kol=int(5)
optimizer = 'time'


def algoritm(name, kol):
    # первый обьект
    first = df_cut.loc[df_cut['название.объекта'] == name].iloc[0,].tolist()
    # класстер первого обьекта
    label = first[3]
    # обьекты этого класстера
    agree = df_cut.loc[df_cut['labels'] == label]
    # убираем  дубликаты
    agree = agree.drop_duplicates()
    # удаляем первый обьект из кластера
    agree = agree.set_index('название.объекта').drop([name], axis=0)
    agree = agree.reset_index('название.объекта')
    # конверт дф в лист
    List = agree.values.tolist()
    # если памятник не находится в радиусе километр то удаляем его из списка
    for i in range(len(List)):
        distance = calculate_distance(first[2], first[1], List[i][2], List[i][1])
        if distance > 10:
            agree = agree.drop(index=i)
    # конверт  новый дф в лист
    List = agree.values.tolist()

    random_landmarks = []

    # добавляем first_landmark в random_landmarks
    landmark = []
    landmark.append(first[0])
    landmark.append(first[1])
    landmark.append(first[2])
    random_landmarks.append(landmark)

    # начало время работы программы
    start = time.time()

    # выберем n-1 памятник рандомно в радиусе 10 км
    while len(random_landmarks) < int(kol):
        if time.time() - start > 0.2:
            sys.exit("недостаточно памятников в радиусе 1км")
        random_index = random.randint(0, len(List) - 1)
        if List[random_index] not in random_landmarks:
            random_landmarks.append(List[random_index])

    # алгоритм кратшайшего пути
    mas = []  # массив длин из пункта А в пункт Б
    dict = {}  # словарь маршрута из  А в Б
    val = [i for i in range(1, len(random_landmarks))]

    for _ in range(len(random_landmarks)):
        mas.append([0] * (len(random_landmarks)))

    for i in range(len(random_landmarks)):
        for j in range(i + 1, len(random_landmarks)):
            orig_node = ox.get_nearest_node(russia_map, (random_landmarks[i][2], random_landmarks[i][1]))

            dest_node = ox.get_nearest_node(russia_map, (random_landmarks[j][2], random_landmarks[j][1]))

            shortest_route = nx.shortest_path(russia_map, orig_node, dest_node,
                                              weight=optimizer)
            # длина маршрута
            a = sum(ox.get_route_edge_attributes(russia_map, shortest_route, 'length'))
            mas[i][j] = round(a)
            mas[j][i] = round(a)
            dict[i, j] = shortest_route
            dict[j, i] = list(reversed(shortest_route))

    comb = []  # комбинации

    import itertools
    perm_set = itertools.permutations(val)
    for i in perm_set:
        a = list(i)
        comb.append(a)

    cord = []  # массив дуг всех маршрутов

    for i in range(len(comb)):
        ride = []
        for j in range(len(comb[i])):
            if j == 0:
                q = [0, comb[i][j]]
            else:
                q = [comb[i][j - 1], comb[i][j]]
            ride.append(q)
        cord.append(ride)

    values = []  # массив длин маршрутов

    for i in range(len(cord)):
        lena = 0
        for j in range(len(cord[i])):
            lena += mas[cord[i][j][0]][cord[i][j][1]]
        values.append(lena)
    # рисуем кратшайший маршрут
    route = []
    min_values = min(values)
    index_short_route = values.index(min_values)
    for i in range(len(cord[index_short_route])):
        if i != len(random_landmarks) - 1:
            route.extend(dict[cord[index_short_route][i][0], cord[index_short_route][i][1]][:-1])
        else:
            route.extend(dict[cord[index_short_route][i][0], cord[index_short_route][i][1]])
    shortest_route_map = ox.plot_route_folium(russia_map, route)
    # добавляем метки
    for i in range(0, len(random_landmarks)):
        start_marker = folium.Marker(
            location=(random_landmarks[i][2], random_landmarks[i][1]),
            popup=(random_landmarks[i][0]),
            icon=folium.Icon(color='green'))
        start_marker.add_to(shortest_route_map)
    print(f'Длина маршрута составляет {min_values} метров!')
    return shortest_route_map
