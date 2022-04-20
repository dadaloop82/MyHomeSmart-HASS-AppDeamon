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
# Logging functions
import module.log as LOG
# Databaase functions
import module.database as DB
# filesystem "exists" from os
from os.path import exists


class main(hass.Hass):

    def entityStateChanged(self, entityName: str, attribute: dict, old: any, new: any, kwargs: dict):
        """Support function to HASS.entityUpdate 

        Args:
            entityName (str):         The name of entity
            attribute (dict):         The attribute of entity (from appDeamon listen_state)
            old (any):                The previous state of this entity
            new (any):                The new state of this entity
            kwargs (dict):            Extra arguments
        """
        _isEditable = False
        if "editable" in kwargs['attrs']:
            _isEditable = kwargs['attrs']['editable']
        HASS.entityUpdate(self, entityName, new, old,
                          attribute, _isEditable, kwargs)

    def initialize(self):
        """Default entrypoint for appDeamon           
        """
        try:
            """ Check DB existence """
            if not exists(CONSTANT.DBPath_History):
                DB.createDB(self, CONSTANT.DBPath_History)

            """ Get usable entities """
            _entities = HASS.get_HASSEntities(
                self,
                UTILITY.getConfigValue(self, "include_entities"),
                UTILITY.getConfigValue(self, "exclude_entities")
            )
            """ Check if are any usable entities """
            if not _entities:
                LOG.LogError(
                    "There are no entities to control or monitor", True)
            LOG.LogInfo(self, ("[ %s ] entities were found to be usable" %
                        len(_entities)))
            """ Subscribe on all entities """
            for _entityData in _entities.items():
                _entityName = _entityData[0]
                _entityAttrs = _entityData[1]
                _entityObj = self.get_entity(_entityName)
                _entityObj.listen_state(
                    self.entityStateChanged, attrs=_entityAttrs['attributes'])
        except Exception as e:
            """ There has been an error """
            LOG.LogError(self, e, True)
