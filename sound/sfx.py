import pygame as pg
from typing import TYPE_CHECKING, Literal, get_args
if TYPE_CHECKING:
    import data_class

SoundClasses = Literal["music", "player_sfx", "shooting", "enemy_sfx", "effect_sfx"]
AllMusicSounds = Literal["title_music", "music_mars", "music_venus", "music_mercury", "music_map", "music_boss"]
AllPlayerSFXSounds = Literal["title_hover", "title_click", "hover", "click", "shop_buy", "lose", "win", "reward", "dramatic_reveal"]
AllShootingSounds = Literal["flare_gun", "heavy_cannon", "heavy_shot", "crystal_shot", "gear_throw", "electrical_shot", "laser_shot", "pistol_shot"]
AllEnemySFXSounds = Literal["damage"]
AllEffectSFXSounds = Literal["coin"]


import logging




###################
#### Main Code ####
###################



class SFX:
    def __init__(self, data: "data_class.Data_class"):
        self.data = data

        # Mixer setup
        self.channel_reservation : dict[SoundClasses, int] = {
            "music": 2,         #  0- 1 : Background Music
            "player_sfx": 10,   #  2-11 : Player SFX (like clicking or shop)
            "shooting": 10,     # 12-21 : Shooting SFX (from towers)
            "enemy_sfx": 10,    # 22-31 : Enemy SFX (like dying)
            "effect_sfx": 10    # 32-41 : Effect SFX (like freezing)
        }
        total_channels_needed : int = sum(self.channel_reservation.values())
        pg.mixer.set_num_channels(total_channels_needed)
        self.channels : dict[SoundClasses, list[pg.mixer.Channel]] = {}
        channel_i : int = -1
        for category, count in self.channel_reservation.items():
            self.channels[category] = []
            for _ in range(count):
                channel_i += 1
                self.channels[category].append(pg.mixer.Channel(channel_i))


        self.sound_category : dict[AllMusicSounds | AllPlayerSFXSounds | AllShootingSounds | AllEnemySFXSounds | AllEffectSFXSounds, SoundClasses] = {} # Define the mapping of sound names to their categories
        for sound_name in get_args(AllMusicSounds):
            if sound_name != "":
                self.sound_category[sound_name] = "music"
        for sound_name in get_args(AllPlayerSFXSounds):
            if sound_name != "":
                self.sound_category[sound_name] = "player_sfx"
        for sound_name in get_args(AllShootingSounds):
            if sound_name != "":
                self.sound_category[sound_name] = "shooting"
        for sound_name in get_args(AllEnemySFXSounds):
            if sound_name != "":
                self.sound_category[sound_name] = "enemy_sfx"
        for sound_name in get_args(AllEffectSFXSounds):
            if sound_name != "":
                self.sound_category[sound_name] = "effect_sfx"


        self.available_channels : dict[SoundClasses, list[pg.mixer.Channel]] = {category: [] for category in get_args(SoundClasses)}


        # Sound loading
        self.current_volume_general : int = 4
        self.current_volume_music : int = 3
        self.current_volume_shot : int = 3
        self.current_volume_player : int = 4
        self.current_volume_other : int = 4

        self.sounds : dict[AllMusicSounds | AllPlayerSFXSounds | AllShootingSounds | AllEnemySFXSounds | AllEffectSFXSounds, pg.mixer.Sound] = {}
        for sound_name in [*get_args(AllMusicSounds), *get_args(AllPlayerSFXSounds), *get_args(AllShootingSounds), *get_args(AllEnemySFXSounds), *get_args(AllEffectSFXSounds)]:
            if str(sound_name) == "":
                continue  # Skip empty sound names
            sound_category : SoundClasses = self.sound_category[sound_name]
            sound_path : str = f"assets/sound/{sound_category}/{sound_name}.ogg"
            self.sounds[sound_name] = pg.mixer.Sound(sound_path)       

        self.current_main_music : AllMusicSounds | None = None 
        self.MAIN_MUSIC_CHANCE : float = 1/500
        self.main_music_tries : int = 0

        self.Auto_volume(force=True)  # Set initial volume for all sounds



    def Auto_volume(self, force: bool = False):

        if (self.current_volume_general != self.data.volume_general or 
            self.current_volume_music != self.data.volume_music or 
            self.current_volume_shot != self.data.volume_shooting or 
            self.current_volume_player != self.data.volume_player or 
            self.current_volume_other != self.data.volume_other) or force:

            self.current_volume_general = self.data.volume_general
            self.current_volume_music = self.data.volume_music
            self.current_volume_shot = self.data.volume_shooting
            self.current_volume_player = self.data.volume_player
            self.current_volume_other = self.data.volume_other
            
            music_volume : float = (self.current_volume_general/4) * (self.current_volume_music/4)*0.5
            shot_volume : float = (self.current_volume_general/4) * (self.current_volume_shot/4)*0.5
            player_volume : float = (self.current_volume_general/4) * (self.current_volume_player/4)
            other_volume : float = (self.current_volume_general/4) * (self.current_volume_other/4) # Effect and Enemy SFX are "other" sounds

            if not force:
                logging.info("Volume changed.")

            for sound_name, sound in self.sounds.items():
                if self.sound_category[sound_name] == "shooting":
                    sound.set_volume(shot_volume)
                elif self.sound_category[sound_name] == "music":
                    sound.set_volume(music_volume)
                elif self.sound_category[sound_name] == "player_sfx":
                    sound.set_volume(player_volume)
                else:
                    sound.set_volume(other_volume)          



    def Main(self):
        self.Auto_volume()

        # Detect unused channels and add them to available_channels
        for category, channels in self.channels.items():
            self.available_channels[category].clear()
            for channel in channels:
                if not channel.get_busy():
                    self.available_channels[category].append(channel)

        if len(self.available_channels["music"]) == self.channel_reservation["music"]:
            self.current_main_music = None  # Reset current main music if all channels are available

        # Main-Music-Handling
        if self.data.in_game:
            if self.current_main_music == None:
                self.main_music_tries += 1
                if self.data.other_random.random() < self.MAIN_MUSIC_CHANCE:
                    title : AllMusicSounds = self.data.path_random.choice(["music_boss", "music_map", "music_mercury", "music_venus", "music_mars"])
                    logging.info(f"Playing main music: '{title.capitalize()}' after {round(self.main_music_tries/60, 0)} quiet seconds.")
                    self.Play_Music(title)
        else: # In title-screen
            if self.current_main_music == None:
                self.Play_Music("title_music")





##################
#### API Code ####
##################





    def Play_Music(self, sound_name: AllMusicSounds, force: bool = False):
        """
        Plays a music sound if there are available channels in the music category.
        The chance of playing the sound is proportional to the number of available channels in that category.

        Parameters:
        - sound_name (AllMusicSounds): The name of the music sound to play.
        - force (bool): Whether to play the sound regardless of channel availability.
        """
        self.current_main_music = sound_name
        self.__Play_sound(sound_name, force)

    def Play_Player_SFX(self, sound_name: AllPlayerSFXSounds, force: bool = False):
        """
        Plays a player sound effect if there are available channels in the player_sfx category.
        The chance of playing the sound is proportional to the number of available channels in that category.

        Parameters:
        - sound_name (AllPlayerSFXSounds): The name of the player sound effect to play.
        - force (bool): Whether to play the sound regardless of channel availability.
        """
        self.__Play_sound(sound_name, force)

    def Play_Shooting_SFX(self, sound_name: AllShootingSounds, force: bool = False):
        """
        Plays a shooting sound effect if there are available channels in the shooting category.
        The chance of playing the sound is proportional to the number of available channels in that category.

        Parameters:
        - sound_name (AllShootingSounds): The name of the shooting sound effect to play.
        - force (bool): Whether to play the sound regardless of channel availability.
        """
        self.__Play_sound(sound_name, force)

    def Play_Enemy_SFX(self, sound_name: AllEnemySFXSounds, force: bool = False):
        """
        Plays an enemy sound effect if there are available channels in the enemy_sfx category.
        The chance of playing the sound is proportional to the number of available channels in that category.

        Parameters:
        - sound_name (AllEnemySFXSounds): The name of the enemy sound effect to play.
        - force (bool): Whether to play the sound regardless of channel availability.
        """
        self.__Play_sound(sound_name, force)

    def Play_Effect_SFX(self, sound_name: AllEffectSFXSounds, force: bool = False):
        """
        Plays an effect sound effect if there are available channels in the effect_sfx category.
        The chance of playing the sound is proportional to the number of available channels in that category.

        Parameters:
        - sound_name (AllEffectSFXSounds): The name of the effect sound effect to play.
        - force (bool): Whether to play the sound regardless of channel availability.
        """
        self.__Play_sound(sound_name, force)

        
    def Kill_all_sounds(self):
        """
        Stop all sound effects immediately.
        One Exception : Music gets faded out. 
        """
        for category, channels in self.channels.items():
            for channel in channels:
                if category == "music":
                    channel.fadeout(4000)  # Fade out music over 4 seconds
                else:
                    channel.stop()





##########################
#### Helper Functions ####
##########################




    def __Play_sound(self, sound_name: AllMusicSounds | AllPlayerSFXSounds | AllShootingSounds | AllEnemySFXSounds | AllEffectSFXSounds, force : bool = False):
        """
        Plays a sound if there are available channels in the corresponding category.
        The chance of playing the sound is proportional to the number of available channels in that category.

        Parameters:
        - sound_name (AllMusicSounds | AllPlayerSFXSounds | AllShootingSounds | AllEnemySFXSounds | AllEffectSFXSounds): The name of the sound to play.
        - force (bool): Whether to play the sound regardless of channel availability.
        """
        if sound_name not in self.sounds:
            logging.warning(f"Sound '{sound_name}' not found. Skipping playback.")
            return


        sound_category : SoundClasses = self.sound_category[sound_name]

        available_amount : int = len(self.available_channels[sound_category])
        total_amount : int = self.channel_reservation[sound_category]
        chance : float = available_amount / total_amount

        if (force and available_amount > 0) or (available_amount > 0 and self.data.other_random.random() <= chance):
            channel : pg.mixer.Channel = self.available_channels[sound_category].pop(0)
            channel.play(self.sounds[sound_name])
        elif force:
            logging.warning(f"Forced playback of sound '{sound_name}' failed due to no available channels in category '{sound_category}'.")


        


        