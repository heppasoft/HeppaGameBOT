from .roles import *
import modules
import random

__all__ = ["Player", "Game"]

class Player:
    id: int = 0
    name: str = ""
    role: Role = None
    votes: int = 0
    is_eliminated: bool = False
    
    def __init__(self, player_id: int, name: str) -> None:
        self.id = player_id
        self.name = name
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return f"Player ( id={self.id}, name={self.name}, role={self.role}, is_eliminated={self.is_eliminated} )"
    
    @property
    def is_moderator(self):
        return self.role is not None and self.role.id == "moderator"

class Game:
    players: list[Player] = []
    current_event: str = "on_eyes_opened"
    roles: dict[str, Role] = {}
    moderator: Player = None
    winner: Role = None
    
    def __repr__(self) -> str:
        return f"Game ( vampires_count={self.roles.get('vampire').player_count}, Players={self.players} )"
    
    def add_player(self, player_id: int, name: str):
        self.players.append(Player(player_id, name))
    
    def get_vampires(self) -> list[Player]:
        return list(filter(lambda p: p.role.id == "vampire", self.players))
    
    def start_game(self, vampires_count: int):
        vampire_role = get_role("vampire")
        self.roles["vampire"]= vampire_role(vampires_count)
        
        villager_role = get_role("villager")
        self.roles["villager"]= villager_role(None)
        
        self.distribute_roles()
    
    def distribute_roles(self):
        vampire_role = self.roles.get("vampire")
        vampire_count = vampire_role.player_count
        
        villager_role = self.roles.get("villager")
        
        for i in range(vampire_count):
            player = random.choice(list(filter(lambda p: p.role == None, self.players)))
            idx = self.players.index(player)
            
            player.role = vampire_role
            
            self.players[idx] = player
        
        for player in list(filter(lambda p: p.role == None, self.players)):
            idx = self.players.index(player)
            
            player.role = villager_role
            
            self.players[idx] = player
    
    @property
    def is_players_roles_distributed(self):
        for player in self.players:
            if player.role is None:
                return False
        
        return True
    
    def set_moderator(self, player_id: int, name: str):
        if self.moderator is not None:
            return
        
        self.moderator = Player(player_id, name)
    
    def open_eyes(self):
        self.current_event = "on_eyes_opened"
    
    def close_eyes(self):
        self.current_event = "on_eyes_closed"
    
    def get_current_event(self):
        return self.current_event
    
    def kill_player(self, player_id: int):
        player = modules.get(self.players, id=player_id)
        idx = self.players.index(player)
        
        player.is_eliminated = True
        
        self.players[idx] = player
    
    def hang_player(self, player_id: int):
        player = modules.get(self.players, id=player_id)
        idx = self.players.index(player)
        
        player.is_eliminated = True
        
        self.players[idx] = player
        
    def vote_player(self, player_id: int):
        player = modules.get(self.players, id=player_id)
        idx = self.players.index(player)
        
        player.votes += 1
        
        self.players[idx] = player
    
    def voting_result(self) -> dict[str, int]:
        votes = {}
        
        players = sorted(self.players, key=lambda p: p.votes)
        
        for player in players:
            votes[player.id] = player.votes
            idx = self.players.index(player)
            player.votes = 0
            self.players[idx] = player
        
        return votes
    
    def check_winner(self):
        vampires = [ player for player in self.players if player.role.id == "vampire" and not player.is_eliminated ]
        villagers = [ player for player in self.players if player.role.id == "villager" and not player.is_eliminated ]
        
        if len(vampires) >= len(villagers):
            self.winner = self.roles.get("vampire")
        else:
            self.winner = self.roles.get("villager")
        
        return self.winner
