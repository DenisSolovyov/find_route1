from trains.models import Train


def dfs_path(graph, start, goal):
    """Функция поиска всех возможных маршрутов
    из одного города в другой. Вариант посещения
    одного и того же города более одного раза
    не рассматривается"""
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex in graph.keys():
            for next_ in graph[vertex] - set(path):
                if next_ == goal:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_]))


def get_graph(qs):
    graph = {}
    for q in qs:
        graph.setdefault(q.from_city_id, set())
        graph[q.from_city_id].add(q.to_city_id)
    return graph


def get_routes(request, form) -> dict:
    context = {'form': form}
    qs = Train.objects.all().select_related('from_city', 'to_city')
    graph = get_graph(qs)
    data = form.cleaned_data
    from_city = data['from_city']
    to_city = data['to_city']
    cities = data['cities']
    traveling_time = data['traveling_time']
    all_ways = list(dfs_path(graph, from_city.id, to_city.id))
    if not len(all_ways):
        raise ValueError('Маршрута удовлетворяющего условиям не существует')
    if cities:
        _cities = [city.id for city in cities]
        ways = []
        for route in all_ways:
            if all(city in route for city in _cities):
                ways.append(route)
        if not ways:
            raise ValueError('Маршрут через эти города невозможен')
    else:
        ways = all_ways
    routes = []
    all_trains = {}
    for q in qs:
        all_trains.setdefault((q.from_city_id, q.to_city_id), [])
        all_trains[(q.from_city_id, q.to_city_id)].append(q)
    for route in ways:
        tmp = {'trains': []}
        total_time = 0
        for i in range(len(route) - 1):
            qs = all_trains[(route[i], route[i + 1])]
            q = qs[0]
            total_time += q.travel_time
            tmp['trains'].append(q)
        tmp['total_time'] = total_time
        if total_time <= traveling_time:
            routes.append(tmp)
    if not routes:
        raise ValueError('Время в пути получилось больше заданного')
    sorted_routes = []
    if len(routes) == 1:
        sorted_routes = routes
    else:
        times = sorted(list(set(r['total_time'] for r in routes)))
        for time in times:
            for route in routes:
                if time == route['total_time']:
                    sorted_routes.append(route)
    context['routes'] = sorted_routes
    context['cities'] = {'from_city': from_city, 'to_city': to_city}
    return context
