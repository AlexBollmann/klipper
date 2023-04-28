# HX711 Support
#
# Copyright (C) 2023 Gareth Farrington <gareth@waves.ky>
#
# This file may be distributed under the terms of the GNU GPLv3 license.

import logging
from . import load_cell

class HX711(load_cell.LoadCellSensor):
    def __init__(self, config):
        self.printer = printer = config.get_printer()
        self.name = config.get_name()
        ppins = printer.lookup_object('pins')
        dout_pin_params = ppins.lookup_pin(config.get('dout_pin'))
        sclk_pin_params = ppins.lookup_pin(config.get('sclk_pin'))
        self.mcu = mcu = dout_pin_params['chip']
        self.oid = mcu.create_oid()
        self.dout_pin = dout_pin_params['pin']
        self.sclk_pin = sclk_pin_params['pin']
        # HX711 sps choices
        self.sps = config.getchoice('sample_rate', {80: 80, 10: 10}, default=80)
        # HX711 gain/channel choices
        self.gain_channel = int(config.getchoice('gain', {'A-128': 1, 'B-32': 2
                                    , 'A-64': 3}, default='A-128'))
        ppins.register_chip(self.name, self)
    #    mcu.register_config_callback(self._build_config)
    #def _build_config(self):
        logging.info("creating HX711 config_hx71x oid=%d dout_pin=%s" \
                                    " sclk_pin=%s gain_channel=%d"
            % (self.oid, self.dout_pin, self.sclk_pin
               , self.gain_channel))
        self.mcu.add_config_cmd("config_hx71x oid=%d dout_pin=%s" \
                                    " sclk_pin=%s gain_channel=%d"
            % (self.oid, self.dout_pin, self.sclk_pin
               , self.gain_channel))
    def get_oid(self):
        return self.oid
    def get_load_cell_sensor_type(self):
        return 'hx71x'
    def get_mcu(self):
        return self.mcu
    def start_capture(self):
        pass # capture cant be stopped/started on these chips
    def stop_capture(self):
        pass # capture cant be stopped/started on these chips
    def get_samples_per_second(self):
        return self.sps

def load_config_prefix(config):
    return HX711(config)