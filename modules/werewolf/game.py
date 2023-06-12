from . import roles
import random


class Player:
    id: int = None
    role: roles.Role = None
    power: int = 0
    
    def __init__(self, id: int, role: (roles.Role|None), game: "Game") -> None:
        self.id = id
        self.role = role
        self.game: Game = game
    
    def __repr__(self) -> str:
        return f"Player ({self.id}, {self.role})"

    def __str__(self) -> str:
        return f"{self.id}"


class Game:
    players: list[Player] = []
    wolves: list[Player] = []
    roless: list[str] = []
    moderator: Player = None
    
    def __init__(self, roless: list[str]) -> None:
        self.roless = roless
    
    @property
    def roleless_players(self):
        players = []
        
        for player in self.players:
            if player.role is None:
                players.append(player)
        
        return players
    
    def add_player(self, id: int):
        self.players.append(Player(id, None, self))
    
    def set_moderator(self, id: int):
        player = Player(id, roles.get_role("moderator")(self), self)
        self.moderator = player
        self.players.append(player)
    
    def distribute_roles(self):
        roless: list[roles.Role] = []
        for role in self.roless:
            rolee = roles.get_role(role)
            roless.append(rolee(self))
            
        for player in self.players:
            idx = self.players.index(player)
            if player.role is not None:
                continue
            
            role = random.choices(roless, weights={r.probability for r in roless})[0]
            print(role.id,role.player_count)
            player.role = role
            self.players[idx] = player
    
    def kill(self, killer: Player, target: Player) -> str:
        self.players.remove(target)
        
        return f"{killer.role.name} bir {target.role.name} öldürdü. Ölen kişi: {target.id}"