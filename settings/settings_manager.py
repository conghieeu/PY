import configparser
import os
from utils.abilities import abilities

class SettingsManager:
    """
    Class to manage application settings.

    This class handles reading, writing, validating, and managing application settings
    stored in a configuration file. It ensures the settings file exists and provides
    methods to read from and write to the settings file.
    """

    def __init__(self, file_name):
        """
        Initializes the SettingsManager instance.

        Args:
            file_name (str): The name of the settings file.
        """
        self.file_name = file_name
        self.config = configparser.ConfigParser()
        self.check_for_settings_file()  # Ensure the settings file exists
        self.read_file()  # Read the settings file
        self.update_values_from_file()  # Update settings from the file

    def check_for_settings_file(self):
        """
        Checks if the settings file exists. If it does not, creates a default settings file.
        """
        if not os.path.exists(self.file_name):
            self.create_default_settings_file()

    def create_default_settings_file(self):
        """
        Creates a default settings file with initial settings.
        """
        self.config['Settings'] = {
            'hero_ability': 'viper_snakebite',
            'valorant_sens': 1,
            'minimum_inactive_time_for_mouse_on_top': 1,
            'allowed_time_to_move_mouse_to_ping': 1,
            'beep_or_tts': 'tts',
            'hotkey': 'f1',
            'xy_tolerance': 3
        }
        with open(self.file_name, 'w') as configfile:
            self.config.write(configfile)

    def read_file(self):
        """
        Reads the settings file.
        """
        self.config.read(self.file_name)

    def fix_corrupted_settings_file(self):
        """
        Fixes a corrupted settings file by creating a new default settings file and updating values.
        """
        self.create_default_settings_file()
        self.update_values_from_file()

    def update_values_from_file(self):
        """
        Updates settings values from the configuration file.

        Reads the settings from the file and updates the internal state of the SettingsManager instance.
        If any setting is missing, it fixes the settings file.
        """
        try:
            settings = self.config['Settings']
            self.valorant_sens = float(settings['valorant_sens'])
            self.minimum_inactive_time_for_mouse_on_top = float(settings['minimum_inactive_time_for_mouse_on_top'])
            self.allowed_time_to_move_mouse_to_ping = float(settings['allowed_time_to_move_mouse_to_ping'])
            self.beep_or_tts = settings['beep_or_tts']
            self.hotkey_button = settings['hotkey']
            self.xy_tolerance = float(settings['xy_tolerance'])
            self.sens_adjustment = self.valorant_sens / 0.623


            # Get the hero ability name from the config and find the corresponding Ability object
            hero_ability_name = self.config.get('Settings', 'hero_ability')
            self.hero_ability = next((ability for ability in abilities if ability.name == hero_ability_name), None)
        except (configparser.NoSectionError, configparser.NoOptionError):
            self.fix_corrupted_settings_file()
