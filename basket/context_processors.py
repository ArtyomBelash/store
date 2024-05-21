from .basket import Basket


def basket(request):
    return {'cart': Basket(request)}
