class Phone:

    def __init__(self, screen, model):
        print("Phone init")
        self.screen = screen
        self.model = model

    def play_music(self):
        print("Phone")


class Player:

    # def __init__(self, music_format='mp3'):
    #     self.music_format = music_format

    def __init__(self, music_format):
        print("Player init")
        self.music_format = music_format

    def play_music(self):
        print(f'Playing music in format {self.music_format}')


class Android(Phone, Player):

    def __init__(self, screen, model, android_name):

        Phone.__init__(self, screen, model)
        Player.__init__(self, "mp3")
        self.android_name = android_name


android = Android(5.5, 'Samsung', 'Robot')
print(android.__dict__)
print(android.play_music())  # почему печатает еще и None ????
