import json


class Level:

    def __init__(self):
        self.waves = {}

    def add_wave(self, wave):
        self.waves[str(len(self.waves))] = wave.wave

    def delete_wave(self, wave_number):
        self.waves.pop(str(wave_number))
        for number in range(wave_number, len(self.waves)):
            self.waves[str(number)] = self.waves.pop(str(number + 1))


class Wave:

    def __init__(self):
        self.wave = {"Unit": {"Zergling": 0, "Roach": 0, "Mutalisk": 0},
                     "delay": 0}

    def add_unit(self, unit, unit_count):
        self.wave["Unit"][unit] = unit_count

    def delete_unit(self, unit):
        self.wave["Unit"][unit] = 0

    def set_delay(self, delay):
        self.wave['delay'] = delay
