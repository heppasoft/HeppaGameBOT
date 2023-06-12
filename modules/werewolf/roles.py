import json

roles_config = json.load(open("modules/werewolf/werewolf_roles.json", encoding="utf-8"))
lang = roles_config["lang"]
lang_name = f"name_{lang}"

class Role:
    id: str = ""
    name: str = ""
    team: str = ""
    aura: str = ""
    dec: str = ""
    probability: int = 100
    player_count: int = 1
    
    def __init__(self, game) -> None:
        self.game = game
        self.name = roles_config[self.id].get(lang_name, self.id.capitalize())
        self.dec = roles_config[self.id]["dec"][lang]
        
    def __repr__(self) -> str:
        return f"Role ({self.name})"

    def __str__(self) -> str:
        return self.name
    
    def on_start(self):
        pass
    
    def on_day(self):
        pass
    
    def on_night(self):
        pass
    
    def on_death(self):
        pass


class Moderator(Role):
    id = "moderator"
    team = "-"
    aura = "-"


class Villager(Role):
    id = "villager"
    team = "villagers"
    aura = "good"
    probability = 80
    
    def __init__(self, game) -> None:
        super().__init__(game)
        self.player_count = int((len(self.game.roleless_players) * 60) / 100)
    
    def on_day(self, target):
        pass


class Werewolf(Role):
    id = "werewolf"
    team = "villains"
    aura = "bad"
    probability = 40
    
    def __init__(self, game) -> None:
        super().__init__(game)
        villagers = []
        
        for player in self.game.players:
            if player.role is not None and player.role.id == "villager":
                villagers.append(player)
        
        print(len(villagers))
        self.player_count = int((len(self.game.players) * 20) / 100)


def get_role(id: str):
    for role in (Moderator, Villager, Werewolf):
        if role.id == id or role.__name__.lower() == id:
            return role