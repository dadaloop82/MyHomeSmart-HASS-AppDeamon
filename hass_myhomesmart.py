#   __  __       _    _                       _____                      _
#  |  \/  |     | |  | |                     / ____|                    | |
#  | \  / |_   _| |__| | ___  _ __ ___   ___| (___  _ __ ___   __ _ _ __| |_
#  | |\/| | | | |  __  |/ _ \| '_ ` _ \ / _ \\___ \| '_ ` _ \ / _` | '__| __|
#  | |  | | |_| | |  | | (_) | | | | | |  __/____) | | | | | | (_| | |  | |_
#  |_|  |_|\__, |_|  |_|\___/|_| |_| |_|\___|_____/|_| |_| |_|\__,_|_|   \__|
#           __/ |
#          |___/
#
# Idea:       dadaloop82 - dadaloop82@gmail.com
# Started:    April 2022
# Github:     https://github.com/dadaloop82/MyHomeSmart-HASS-AppDeamon
# License:    GPLv2 (https://raw.githubusercontent.com/dadaloop82/MyHomeSmart-HASS-AppDeamon/main/LICENSE)
# Version     2.0α
#
# Today we can enjoy several devices called "smart"; devices that seem to possess reasoning, logic and
# deduction skills in performing seemingly spontaneous actions. In reality, this is not the case at all,
# each device is programmed to do actions under certain conditions, without any understanding of what it is
# doing and the possible consequence that such actions can do. For example, smart speakers simply read what
# they find on the web, but they don't know if what they read is right or they cause the user to do the
# wrong thing. A smart television is not smart, it just offers more opportunities for digital services.
# And so on.
# Giving intelligence to home automation means giving a logical and comprehensive reasoning to the action
# that the home automation system should do to reach a certain objective.
#

# Essential library for communicating with HASS
import hassapi as hass
# Constants
import module.constant as CONSTANT
# Variables
import module.variables as VARIABLES
# Utility
import module.utility as UTILITY
# Home Assistant functions
import module.hass as HASS


class main(hass.Hass):

    def initialize(self):

        _entities = HASS.get_HASSEntities(
            self,
            UTILITY.getConfigValue(self, "include_entities"),
            UTILITY.getConfigValue(self, "exclude_entities")
        )
        self.log(_entities)
