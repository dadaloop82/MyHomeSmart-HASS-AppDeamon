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

    # Global Class variable
    lastNodeID = -1                     # last Entity id Changed
    lastEditableEntity = -1

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
        _entityID, _nodeID = HASS.entityUpdate(self, DB, entityName, new, old,
                                               attribute, _isEditable, self.lastNodeID, self.lastEditableEntity, kwargs)

        LOG.info(self, "[lastNodeID] %s: [lastEditableEntity] %s -> [_entityID] %s" %
                 (self.lastNodeID, self.lastEditableEntity, _entityID))

        self.lastNodeID = _nodeID

        if(_isEditable and _entityID != self.lastEditableEntity):
            self.lastEditableEntity = _entityID
    def initialize(self):
        """Default entrypoint for appDeamon           
        """

        try:

            """ Check DB existence and connect them """
            if not exists(CONSTANT.DB_EntityState):
                DB.create(self, CONSTANT.DB_EntityState)
            DB.connect(self, CONSTANT.DB_EntityState,
                       CONSTANT.DB_EntityState)
            if not exists(CONSTANT.DB_CauseEffect):
                DB.create(self, CONSTANT.DB_CauseEffect)
            DB.connect(self, CONSTANT.DB_CauseEffect,
                       CONSTANT.DB_CauseEffectName)

            """ Get usable entities """
            _entities = HASS.get_HASSEntities(
                self,
                UTILITY.getConfigValue(self, "include_entities"),
                UTILITY.getConfigValue(self, "exclude_entities")
            )

            """ Check if are any usable entities """
            if not _entities:
                LOG.error(self,
                          "There are no entities to control or monitor, check apps.yaml", True)
            LOG.info(self, ("[ %s ] entities were found to be usable" %
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
            LOG.error(self, e, True)
