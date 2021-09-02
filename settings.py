class Settings:
    def __init__(self):
        # Display settings:
        self.screen_width, self.screen_height = 1200, 800
        self.caption = "Space Shooter"
        self.fps = 100
        # Menu objects settings:-
        self.update_magnitude = 100
        # Player Settings:-
        self.player_velocity = 10
        self.player_ship_size = (80, 80)
