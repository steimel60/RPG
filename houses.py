class HogwartsHouse():
    def __init__(self, name, founder, color, secondary_color):
        self.school = 'Hogwarts'
        self.name = name
        self.founder = f'{founder} {name}'
        self.color = color
        self.secondary_color = secondary_color

SlytherinHouse = HogwartsHouse('Slytherin', 'Salazar', (42,98,61), (170,170,170))
GryffindorHouse = HogwartsHouse('Gryffindor', 'Godric', (174,0,1), (238,186,48))
HufflepuffHouse = HogwartsHouse('Hufflepuff', 'Helga', (236,185,57), (55,46,41))
RavenclawHouse = HogwartsHouse('Ravenclaw', 'Rowena', (34,47,91), (93,93,93))
