class showdowner:

    def __init__(self, name, img, type, hp, moves):
        self.name = name
        self.img = img
        self.type = type
        self.hp = hp
        self.moves = moves if moves else ["Basic Attack"]

    def __str__(self):
        str = ""
        str += f"Name: {self.name}\n"
        str += f"Type: {self.type}\n"
        str += f"HP: {self.hp}\n"
        str += f"Moves: {', '.join(self.moves)}\n"
        return str

    def to_dict(self):
        d = {
            "Name": self.name,
            "Img": self.img,
            "Type": self.type,
            "HP": self.hp,
            "Moves": self.moves
        }
        return d

    @staticmethod
    def from_dict(d):
        old_self = showdowner(
            d['Name'], 
            d['Img'], 
            d['Type'], 
            d['HP'], 
            d['Moves']
        )
        return old_self

    def attack(self, move_name, other, universe="Pokemon"):
        # This method is now handled in the Flask route with type advantage
        # Keeping it for backward compatibility
        pass