from modules import werewolf

game = werewolf.Game(["werewolf","villager"])
game.set_moderator(1)
for i in range(2, 11):
    game.add_player(i)

game.distribute_roles()
print(game.players)