import datetime
from Hub import Hub
from Route import Route
from Manager import Manager

if __name__ == "__main__":
    h1 = Hub("Продуктовый склад")
    h2 = Hub("Шестёрочка")
    h3 = Hub("Продуктовый магазин")

    print(h1._id, h3._id)

    p = Route(h1, h3, datetime.time(hour=10, minute=5), datetime.time(hour=10, minute=25))

    print(p)

    m = Manager()
    m.add_point(h1)
    m.add_point(h2)
    print(m.points)

    m.add_route(p)
    m.add_route(point_a=h3, point_b=h2, ets=datetime.time(hour=18, minute=0), eta=datetime.time(hour=19, minute=5))
    m.add_route(point_a=h3, point_b=h1, ets=datetime.time(hour=13, minute=0), eta=datetime.time(hour=13, minute=5))

    print(m.routs)

    print(m.find_fastest_route(h1, h2))

    m.add_route(point_a=h3, point_b=h2, ets=datetime.time(hour=12, minute=0), eta=datetime.time(hour=13, minute=0))
    print(m.find_fastest_route(h1, h2))

    m.add_route(point_a=h3, point_b=h2, ets=datetime.time(hour=10, minute=0), eta=datetime.time(hour=11, minute=0))
    print(m.find_fastest_route(h1, h2))