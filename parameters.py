import json


class Parameters:
    def __init__(self) -> None:
        super().__init__()

        self._SAMPLING_FREQUENCY: int = 48000
        self._SAMPLES_PER_BUFFER: int = 1024 # 20 ms

        self._MIN_SINE_WAVE_FREQUENCY: int = 1
        self._MIN_VOLUME: float = 1.0

        self._MAX_SINE_WAVE_FREQUENCY: int = 500
        self._MAX_VOLUME: float = 20.0
        
        self._DEFAULT_SINE_WAVE_FREQUENCY: int = 220
        self._DEFAULT_ADD_NOISE: bool = True
        self._DEFAULT_VOLUME: float = self._MIN_VOLUME
                
        self._sine_wave_frequency: int = self._DEFAULT_SINE_WAVE_FREQUENCY
        self._add_noise: bool = self._DEFAULT_ADD_NOISE
        self._volume: float = self._DEFAULT_VOLUME
        
        self._CONFIG_FILE_NAME: str = "config.json"
        self._SINE_WAVE_FREQUENCY_JSON_KEY: str = "sine_wave_frequency"
        self._ADD_NOISE_JSON_KEY: str = "add_noise"
        self._VOLUME_JSON_KEY: str = "volume"

        load_status: bool = self._load()
        if load_status is False:
            self._save()

    def _load(self) -> bool:
        load_status: bool = True

        try:
            with open(self._CONFIG_FILE_NAME, "r") as config_file:
                parameters_from_config_file = json.load(config_file)

                sine_wave_frequency_from_config_file: int = \
                    parameters_from_config_file[
                        self._SINE_WAVE_FREQUENCY_JSON_KEY]
                
                add_noise_from_config_file: bool = \
                    parameters_from_config_file[self._ADD_NOISE_JSON_KEY]
                
                volume_from_config_file: float = \
                    parameters_from_config_file[self._VOLUME_JSON_KEY]
                
                print("Parameters are loaded from config file successfully.")
                
                # Check parameters.
                result = self._check_sine_wave_frequency(
                    sine_wave_frequency=sine_wave_frequency_from_config_file)
                if result is True:
                    self._sine_wave_frequency = \
                        sine_wave_frequency_from_config_file
                else:
                    print("ERROR! Using default \"sine wave frequency\"!")
                    self._sine_wave_frequency = \
                        self._DEFAULT_SINE_WAVE_FREQUENCY
                    load_status = False

                result = self._check_add_noise(
                    add_noise=add_noise_from_config_file)
                if result is True:
                    self._add_noise = add_noise_from_config_file
                else:
                    print("ERROR! Using default \"add noise\"!")
                    self._add_noise = self._DEFAULT_ADD_NOISE
                    load_status = False

                result: bool = self._check_volume(
                    volume=volume_from_config_file)
                if result is True:
                    self._volume = volume_from_config_file
                else:
                    print("ERROR! Using default \"volume\"!")
                    self._volume = self._DEFAULT_VOLUME
                    load_status = False

        except (OSError, json.JSONDecodeError, KeyError) as e:
            print(type(e))
            print(e)
            print("ERROR! Could not load parameters from config file!")
            print("ERROR! Using default parameters!")
            self._sine_wave_frequency = self._DEFAULT_SINE_WAVE_FREQUENCY
            self._add_noise = self._DEFAULT_ADD_NOISE
            self._volume = self._DEFAULT_VOLUME
            load_status = False
    
        return load_status

    def _save(self) -> None:
        parameters_to_config_file = {
            self._SINE_WAVE_FREQUENCY_JSON_KEY:self._sine_wave_frequency,
            self._ADD_NOISE_JSON_KEY:self._add_noise,
            self._VOLUME_JSON_KEY:self._volume
        }

        try:
            with open(self._CONFIG_FILE_NAME, "w") as config_file:
                json.dump(parameters_to_config_file, config_file, indent=4)
                print("Parameters are saved to config file successfully.")

        except OSError as e:
            print(type(e))
            print(e)
            print("ERROR! Could not save parameters to config file!")

    def _check_sine_wave_frequency(self, sine_wave_frequency) -> bool:
        if ((sine_wave_frequency is not None) and
            (isinstance(sine_wave_frequency, int)) and
            (sine_wave_frequency >= self._MIN_SINE_WAVE_FREQUENCY) and
            (sine_wave_frequency <= self._MAX_SINE_WAVE_FREQUENCY)):
            print("\"Sine wave frequency\" is valid.")
            return True
        else:
            print("ERROR! \"Sine wave frequency\" is invalid! "
                  "\"Sine wave frequency\" must be int! "
                  "\"Sine wave frequency\" must be between "
                  f"{self._MIN_SINE_WAVE_FREQUENCY} and {self._MAX_SINE_WAVE_FREQUENCY}!")
            return False

    def _check_add_noise(self, add_noise) -> bool:
        if ((add_noise is not None) and
            (isinstance(add_noise, bool))):
            print("\"Add noise\" is valid.")
            return True
        else:
            print("ERROR! \"Add noise\" is invalid! "
                  "\"Add noise\" must be bool!")
            return False
    
    def _check_volume(self, volume) -> bool:
        if ((volume is not None) and
            (isinstance(volume, (int, float))) and
            (volume >= self._MIN_VOLUME) and
            (volume <= self._MAX_VOLUME)):
            print("\"Volume\" is valid.")
            return True
        else:
            print("ERROR! \"Volume\" is invalid! "
                  "\"Volume\" must be int or float! "
                  "\"Volume\" must be between "
                  f"{self._MIN_VOLUME} and {self._MAX_VOLUME}!")
            return False

    @property
    def sampling_frequency(self) -> int:
        return self._SAMPLING_FREQUENCY

    @property
    def samples_per_buffer(self) -> int:
        return self._SAMPLES_PER_BUFFER
 
    @property
    def sine_wave_frequency(self) -> int:
        return self._sine_wave_frequency
    
    @sine_wave_frequency.setter
    def sine_wave_frequency(self, new_sine_wave_frequency: int) -> None:
        result: bool = self._check_sine_wave_frequency(new_sine_wave_frequency)
        if result is True:
            self._sine_wave_frequency = new_sine_wave_frequency
        else:
            print("ERROR! Using default \"sine wave frequency\"!")
            self._sine_wave_frequency = self._DEFAULT_SINE_WAVE_FREQUENCY
        self._save()
    
    @property
    def add_noise(self) -> bool:
        return self._add_noise
    
    @add_noise.setter
    def add_noise(self, new_add_noise) -> None:
        result: bool = self._check_add_noise(new_add_noise)
        if result is True:
            self._add_noise = new_add_noise
        else:
            print("ERROR! Using default \"add noise\"!")
            self._add_noise = self._DEFAULT_ADD_NOISE
        self._save()
    
    @property
    def volume(self) -> float:
        return self._volume
    
    @volume.setter
    def volume(self, new_volume: float) -> None:
        result: bool = self._check_volume(new_volume)
        if result is True:
            self._volume = new_volume
        else:
            print("ERROR! Using default \"volume\"!")
            self._volume = self._DEFAULT_VOLUME
        self._save()