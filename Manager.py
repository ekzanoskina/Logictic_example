from Route import Route
import datetime

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
                           eta=datetime.time(hour=23, minute=59,
                                             second=59)):  # если время, за которое нужно доставить не указано, считаем, что нужно доставить в течение дня
        found_ways = dict()  # hub: (eta, last_route) сюда собираем все отработанные точки
        found_ways[point_a] = (ets, None)  # если мы придем в None, значит, что мы восстановили весь путь
        '''добавление всех путей из вершин во вне, но не друг в друга
        while True:
            routes = list()
            for h in found_ways.keys():
                for r in self.routs[h]:
                    _from, _to = r.get_points()
                    if _to not in found_ways.keys(): #проверяем, что этой вершины нет в нашем спсике
                        routes.append(r)
        '''
        '''Но нам нужно знать не все ребра, а только то ребро, которое доставит нас в необходимую точку максимально рано'''

        while True:
            fastest_route = None
            fastest_eta = datetime.time(hour=23, minute=59, second=59) #конец дня, берем как максимальное время, чтобы любое другое было раньше него в пределах одного дня

            for h in found_ways.keys():
                earliest_ets = found_ways[h][0] # время прибытия из предыдущей точки - самое раннее время начала движения из текущей точки
                for r in self.routs[h]: # берутся routes для данного хаба, которые были добавлены методом add_route
                    _ets, _eta = r.get_timings() # время начала и конца для текущего рута
                    if earliest_ets > _ets: # если время начала рута раньше, чем мы пришли в эту точку, то мы пропускаем этот рут, как неподходящий
                        continue
                    _from, _to = r.get_points()
                    if _to not in found_ways.keys():
                        if _eta < fastest_eta:
                            fastest_route = r
                            fastest_eta = _ets

            if fastest_route is None: # если нет ни одного маршрута в непройденную вершину
                raise Exception("Не найдена следующая вершина")

            _from, _to = fastest_route.get_points()
            _ets, _eta = fastest_route.get_timings()

            found_ways[_to] = (_eta, fastest_route)
            if _to is point_b:
                break

        if found_ways[point_b][0] > eta:
            return None

        way = list()
        current = point_b

        while found_ways[current][1] is not None:
            route = found_ways[current][1]
            current, _to = route.get_points()
            way.append(route)

        way.reverse()

        return way