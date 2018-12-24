
class Knowledge:
    def __init__(self, condition, conclusion):
        self.condition = condition
        self.conclusion = conclusion

    def print(self):
        print(self.condition)
        print('->', self.conclusion)
        print()


def generate_base():
    base = [Knowledge({'класс': 'духовые', 'корпус': 'канал', 'механизм': 'дутье'},
                      ('семейство', 'трубы')),
            Knowledge({'класс': 'духовые', 'корпус': 'язычок', 'механизм': 'сжатие-разжатие'},
                      ('семейство', 'ручные гармоники')),
            Knowledge({'класс': 'духовые', 'корпус': 'язычок', 'механизм': 'дуьте'},
                      ('семейство', 'губные гармоники')),
            Knowledge({'класс': 'струнные', 'крепление струн': 'вдоль деки'},
                      ('семейство', 'лютни')),
            Knowledge({'класс': 'струнные', 'крепление струн': 'поперек деки'},
                                                         ('семейство', 'цитры')),

            Knowledge({'класс': 'ударные', 'корпус': 'рамка', 'механизм': 'дутье'},
                      ('инструмент', 'варган')),
            Knowledge({'надкласс': 'собственно духовые', 'корпус': 'клавиши', 'механизм': 'дутье'},
                      ('инструмент', 'орган')),

            Knowledge({'тип': 'Идиофоны'}, ('класс', 'ударные')),
            Knowledge({'тип': 'Мембранофоны'}, ('класс', 'ударные')),
            Knowledge({'тип': 'Аэрофоны'}, ('класс', 'духовые')),
            Knowledge({'тип': 'Хордофоны'}, ('класс', 'струнные')),
            Knowledge({'тип': 'Аэрофоны'}, ('надкласс', 'собственно духовые')),
            Knowledge({'тип': 'Аэрофоны'}, ('надкласс', 'свободные аэрофоны'))]

    return base
