class showdowner:

    def __init__(self, name, atk, hp):
        self.name = name
        self.atk = atk
        self.hp = hp

    def __str__(self):
        str = ""
        str += f"name: {self.name}\n"
        str += f"atk: {self.atk}\n"
        str += f"hp: {self.hp}\n"
        return str
    
    def to_dict(self):
        d = {"name": self.name, 
             "atk": self.atk,
             "hp": self.hp}
        return d
    
    @staticmethod
    def from_dict(d):
        old_self = showdowner(d['name'], d['atk'], d['hp'])
        return old_self

    def attack(self, other):
        other.hp -= self.atk