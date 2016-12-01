#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import uniflex_module_wifi_intel

'''
    Direct module test; without framework.
    Req.: Intel WiFi
'''
if __name__ == '__main__':

    wifi = uniflex_module_wifi_intel.Iwl5300Module()

    wifi.my_start_function()

    csi = wifi.get_csi(3)

    print(csi.shape)

    time.sleep(2)

    wifi.my_stop_function()
