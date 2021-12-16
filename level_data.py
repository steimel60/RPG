from settings import *




class LevelDataLibrary():
    def __init__(self):
        self.current_music = None
        self.default_music = path.join(music_folder, 'the_field_of_dreams.mp3')
        self.level_data_dict = {
            'test' : {
                'Music' : path.join(music_folder, 'the_field_of_dreams.mp3'),
                'Music Volume' : 1
            },
            'indoor1' : {
                'Music' : path.join(music_folder, 'shop_music.mp3'),
                'Music Volume' : .4
            },
            'BookShop' : {
                'Music' : path.join(music_folder, 'shop_music.mp3'),
                'Music Volume' : .4
            }
        }

    def get_level_music(self, level):
        if level in self.level_data_dict:
            print('GET FROM DICT')
            try:
                print(self.level_data_dict[level]['Music'])
                return self.level_data_dict[level]['Music']
            except:
                print('EXCEPTION')
                return self.default_music
        else:
            print("ELSE")
            return self.default_music

    def get_music_volume(self, level):
        #Used to keep volumes about even
        return self.level_data_dict[level]['Music Volume']

    def set_current_music(self, music_path):
        self.current_music = music_path
