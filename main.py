import datetime


class Hub:
    _id = -1
    _name = ''
    tracks = list()
    __id_counter__ = 0

    def __init__(self, name):
        self._id = self.__class__.__id_counter__
        self.__class__.__id_counter__ += 1
        self._name = name

    def __str__(self):
        return f'Точка {self._name} c id {self._id}'

    def __hash__(self):
        return self._id

    def __repr__(self):
        return f'[{self._name}: {self._id}]'

    def get_name(self):
        return self._name


class Route:
    _start = None
    _end = None
    _ets = datetime.time()
    _eta = datetime.time()

    def __init__(self, start, end, ets, eta):
        self._start = start
        self._end = end
        self._ets = ets # estimated time of start
        self._eta = eta # estimated time of arrival
        self._estimated_time = (datetime.datetime.combine(datetime.date.today(), eta)
                                - datetime.datetime.combine(datetime.date.today(), ets))

    def __str__(self):
        return f"Путь из {self._start.get_name()} в {self._end.get_name()}, время поездки: {self._estimated_time}"

    def __repr__(self):
        return f'[{self._start.get_name()}: {self._ets} -> {self._end.get_name()}: {self._eta}]'
    def get_points(self):
        return self._start, self._end
    def get_timings(self):
        return self._ets, self._eta

h1 = Hub('продукты')
h2 = Hub('товары')
print(h1._id, h2._id)

r = Route(h1, h2, datetime.time(hour=10, minute=5), datetime.time(hour=10, minute=25))
print(r)

'''
Менеджер - объект, который хранит логику общения с объектами
'''


class Manager:
    points = set()
    routs = dict()

    def __init__(self):
        'Для каждого объекта задаются свои, чтобы можно было поставить какие-то ограничения для определенных видов товаров и в целом распараллелить систему'
        self.points = set()
        self.routs = dict()

    def add_point(self, point):
        self.points.add(point)

    def add_route(self, route: Route = None, point_a=None, point_b=None, ets=datetime.time(), eta=datetime.time()):
        if route is not None:
            point_a, point_b = route.get_points()
        elif point_a is not None and point_b is not None:
            route = Route(point_a, point_b, ets, eta)
        if point_a not in self.points:
            self.points.add(point_a)
        if point_b not in self.points:
            self.points.add(point_b)

        if point_a not in self.routs:
            self.routs[point_a] = list()
        self.routs[point_a].append(route)

    def find_fastest_route(self, point_a, point_b, ets=datetime.time(),
                           eta=datetime.time(hour=23, minute=59, second=59)): #если время, за которое нужно доставить не указано, считаем, что нужно доставить в течение дня
        found_ways = dict()  # hub: (eta, last_route)
        found_ways[point_a] = (ets, None) #если мы придем в None, значит, что мы восстановили весь путь
        while True:
            '''добавление всех путей из вершин во вне, но не друг в друга'''
            routes = list()
            for h in found_ways.keys():
                for r in self.routs[h]:
                    _from, _to = r.get_points()
                    if _to not in found_ways.keys(): #проверяем, что этой вершины нет в нашем спсике
                        routes.append(r)

            '''Но нам нужно знать не все ребра, а только то ребро, которое доставит нас в необходимую точку максимально быстро'''
            fastest_route = None
            fastest_ets = datetime.time(hour=23, minute=59, second=59)

            for h in found_ways.keys():
                latest_ets = found_ways[h][0]
                for r in self.routs[h]:
                    _ets, _eta = r.get_timings()
                    if latest_ets > _ets:
                        continue
                    _from, _to = r.get_points()
                    if _to not in found_ways.keys():
                        if _ets < fastest_ets:
                            fastest_route = r
                            fastest_ets = _ets


m = Manager()
m.add_point(h1)
m.add_point(h2)
print(m.points)
m.add_route(r)
m.add_route(point_a=h1, point_b=h2, ets=datetime.time(hour=10, minute=5), eta=datetime.time(hour=10, minute=25))
print(m.routs)