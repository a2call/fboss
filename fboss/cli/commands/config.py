#
#  Copyright (c) 2004-present, Facebook, Inc.
#  All rights reserved.
#
#  This source code is licensed under the BSD-style license found in the
#  LICENSE file in the root directory of this source tree. An additional grant
#  of patent rights can be found in the PATENTS file in the same directory.
#
# @lint-avoid-pyflakes2
# @lint-avoid-python-3-compatibility-imports

import json

from fboss.cli.commands import commands as cmds
from neteng.fboss.ttypes import FbossBaseError

class GetConfigCmd(cmds.FbossCmd):
    def run(self, config_type):
        if config_type == 'ctrl':
            self._client = self._create_ctrl_client()
        resp = self._client.getRunningConfig()

        if not resp:
            print("No Config Info Found")
            return
        parsed = json.loads(resp)
        print(json.dumps(parsed, indent=4, sort_keys=True,
                         separators=(',', ': ')))


class ReloadConfigCmd(cmds.FbossCmd):
    """
    Command to instruct agent to reload its own config, as if it is restarting,
    but without restarting.
    """
    def run(self):
        try:
            self._client = self._create_ctrl_client()
            self._client.reloadConfig()
            print("Config reloaded")
            return
        except FbossBaseError as e:
            print('Fboss Error: ' + e)
            return 2