class Role:
    id: str = ""
    name: str = ""
    dec: str = ""
    player_count: int = 1
    actions: dict[str, list] = {
        "on_eyes_opened": [],
        "on_eyes_closed": []
    }
    
    def __init__(self, player_count: int) -> None:
        self.player_count = player_count
        
    def __repr__(self) -> str:
        return f"Role ( {self.name} )"

    def __str__(self) -> str:
        return self.name
    
    def get_actions(self, event_name: str):
        return self.actions.get(event_name, None)
    
    def do_action(self, action_name: str, game):
        event_name = "on_eyes_opened" if action_name in self.actions["on_eyes_opened"] else "on_eyes_closed"
        event = getattr(self, event_name)
        
        return event(game)
    
    def on_eyes_opened(self, action_name: str, game):
        if action_name not in self.actions["on_eys_opened"]:
            return
    
    def on_eyes_closed(self, action_name: str, game):
        pass
    
    def on_death(self, game):
        pass

class Moderator(Role):
    id = "moderator"
    name = "Yönetici"
    dec = "Oyunun yötenen kişisin."
    
    def __init__(self) -> None:
        pass

class Vampire(Role):
    id = "vampire"
    name = "Vampir"
    dec = "Bir vampirsin ve geriye vapirlerin sayısı kadar köylü kalıncaya dek köylüleri kandırmalı ve oylama ile astırman gerekiyor."
    actions: dict[str, list] = {
        "on_eyes_opened": ["vote"],
        "on_eyes_closed": []
    }

class Villager(Role):
    id = "villager"
    name = "Köylü"
    dec = "Bir köylüsün ve oylama ile süphelileri asıp vampirleri bulman gerekiyor."
    actions: dict[str, list] = {
        "on_eyes_opened": ["vote"],
        "on_eyes_closed": ["kill"]
    }

def get_role(id: str):
    for role in (Moderator, Villager, Vampire):
        if role.id == id or role.__name__.lower() == id:
            return role