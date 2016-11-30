import logging
import inspect
import subprocess

import matlab.engine
import numpy as np

from uniflex.core import modules
import uniflex_module_wifi
from uniflex.core import exceptions


__author__ = "Anatolij Zubow"
__copyright__ = "Copyright (c) 2015, Technische Universität Berlin"
__version__ = "0.1.0"
__email__ = "{zubow}@tkn.tu-berlin.de"


"""
    WiFi module for Intel 5300 chipsets patched with the driver from
    http://dhalperi.github.io/linux-80211n-csitool/

    Note: this module requres the Matlab Python engine:
    https://de.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html
"""
class Iwl5300Module(uniflex_module_wifi.WifiModule):
    def __init__(self):
        super(Iwl5300Module, self).__init__()
        self.log = logging.getLogger('Iwl5300Module')


    @modules.on_start()
    def my_start_function(self):
        self.eng = matlab.engine.start_matlab()


    @modules.on_exit()
    def my_stop_function(self):
        self.eng.quit()


    def get_csi(self, num_samples):
        """
        Reads the next csi values.
        :param num_samples: the number of samples to read
        :return: the csi values
        """
        res = {}

        try:
            tempfile = '/tmp/out'

            # 1. userland netlink
            cmd = 'log_to_file_max ' + tempfile + ' ' + str(num_samples)
            [rcode, sout, serr] = self.run_command(cmd)

            # 2. read from file
            csi_trace = self.eng.read_bf_file(tempfile)

            for ii in range(num_samples):
                csi_entry = csi_trace[ii]
                csi = self.eng.get_scaled_csi(csi_entry)
                data = self.eng.squeeze_csi_data(csi)

                mat = np.array(data._data).reshape(data.size[::-1]).T
                res[ii] = mat
                #csi_ant_1 = mat[:, 0]
                #csi_ant_2 = mat[:, 1]
                #csi_ant_3 = mat[:, 2]

        except Exception as e:
            self.log.fatal("Failed to get CSI: %s" % str(e))
            raise exceptions.FunctionExecutionFailedException(
                func_name=inspect.currentframe().f_code.co_name,
                err_msg='Failed to get CSI: ' + str(e))

        return res