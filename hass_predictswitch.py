import hassapi as hass
import datetime
import os
import json

from dateutil import tz
from os.path import exists


# Constant
# E_DEBUG = "INFO"
E_DEBUG = "DEBUG"
E_INFO = "INFO"
E_WARNING = "WARNING"
E_ERROR = "ERROR"

# 2021-08-20T14:43:40+00:00
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S+00:00"
ALT_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f+00:00"
ONPERIOD_DATETIME_FORMAT = "%H:%M"
MODELPATH = "models"

# Object
_datetime = datetime.datetime
_currentfolder = os.path.dirname(os.path.abspath(__file__))
_currentDate = _datetime.now()
# HassPredictSwitch Class


class HassPredictSwitch(hass.Hass):

    # Log function
    def Log(self, msg, level=E_INFO, variable=None):
        if level == E_ERROR:
            self.log(f"! {msg} !", level=level,  stack_info=True)
        else:
            self.log(f"[ {msg} ]", level=level)

    # Utility Class
    class Utility:
        def __init__(self, hass):
            self._hass = hass
            self._log = hass.Log

        def convertdatatime(self, datatimeString):
            if "." in datatimeString:
                datatimeString = _datetime.strptime(
                    datatimeString, ALT_DATETIME_FORMAT).strftime(DATETIME_FORMAT)
            a = self._hass.parse_utc_string(datatimeString)
            b = _datetime.utcfromtimestamp(a)
            return b

        def getdifferncedate(self, date, keytime, value):
            if keytime == 'days':
                return date - datetime.timedelta(days=value)
            return None

        def stringisnumber(self, string):
            try:
                float(string)
                return True
            except:
                return False

        def setifnotexist(self, objvar, key, initvalue):
            if key in objvar:
                return objvar
            objvar[key] = initvalue
            return objvar

    # Config Class

    class Config:
        def __init__(self, hass):
            self._config = hass.args["config"]
            self._hass = hass
            self._log = hass.Log

        def Get(self, key):
            try:
                if type(key) == str:
                    return self._config[key]
                if type(key) == list:
                    _ret = self.Get(key[0])
                    for el in key[1:]:
                        _ret = _ret[el]
                    return _ret
                else:
                    return None
            except:
                self._log(f"{key} not found in config", E_ERROR)

    # initialize Class
    def initialize(self):
        self.Log("starting", E_INFO)

        # set Class
        config = self.Config(self)
        utility = self.Utility(self)

        # set Constant
        self.TIMEZONE = tz.gettz(config.Get("timezone"))

        # set Variables
        # bt = baseentity
        # bo = basedOnEntities
        entityStates = {'bt': {}, 'bo': {}}
        baseswitch_historys = []
        averageObject = {}
        isOnStatePeriod = {'state': False, 'datetime': None}
        isDataLoadedFromFile = False
        dayHistory = config.Get('historyday')

        for event in config.Get('predictsevent'):

            # get baseswitch
            baseswitch = config.Get(['predictsevent', event, 'basewitch'])

            # check if model is already saved
            fileName = os.path.join(_currentfolder, MODELPATH, f"{event}.json")

            # set the startDate of events
            eventsHistoryStartDate = _currentDate

            # set the endDate of events
            eventsHistoryEndDate = utility.getdifferncedate(
                _currentDate.replace(hour=23, minute=59), "days", dayHistory)

            if exists(fileName):

                # if the file exist, read the json data (model)
                self.Log(f"<{event}> model already exist - load and use them ")
                fileEventCached = open(fileName,)

                # put the data on entityStates variable
                entityStates = json.load(fileEventCached)

                # close file
                fileEventCached.close()

                # set the savedModelEventsHistoryStartDate|EndDate and the flag in isDataLoadedFromFile
                savedModelEventsHistoryEndDate = _datetime.strptime(
                    entityStates['updatedate'][0], DATETIME_FORMAT)
                savedModelEventsHistoryStartDate = _datetime.strptime(
                    entityStates['updatedate'][1], DATETIME_FORMAT)
                isDataLoadedFromFile = True

            # get history of baseswitch
            self.Log(f"ask baseSwitch: {baseswitch} history ", E_DEBUG)

            # calculate che number of cycles
            cycle = int(dayHistory/10)+1

            # start cycle
            for number in range(0, cycle):

                # calculate start and end period
                startDayPeriod = number*10
                endDayPeriod = startDayPeriod+10

                # if exceed, get the value in config
                if endDayPeriod > dayHistory:
                    endDayPeriod = dayHistory

                # calculate date
                endDate = utility.getdifferncedate(
                    _currentDate.replace(hour=23, minute=59), "days", startDayPeriod)
                startDate = utility.getdifferncedate(
                    _currentDate.replace(hour=00, minute=00), "days", endDayPeriod)

                self.Log(f"Date requested: {startDate} - {endDate}", E_DEBUG)
                self.Log(
                    f"Date cached: {savedModelEventsHistoryStartDate} - {savedModelEventsHistoryEndDate}", E_DEBUG)

                # if is file loaded, check if the startDate are NOT between the already laoaded data
                if(isDataLoadedFromFile and startDate > savedModelEventsHistoryStartDate):
                    startDate = savedModelEventsHistoryEndDate

                # check if startDate is greater than enDate -> the data must be loaded from file
                if startDate >= endDate:
                    self.Log(
                        f"data from cache: {startDayPeriod}/{endDayPeriod}", E_INFO)

                else:

                    # get history for this timeslot
                    self.Log(
                        f"parsing and analyze history data (days: {startDayPeriod}/{endDayPeriod})", E_INFO)

                    history = self.get_history(
                        entity_id=baseswitch, start_time=startDate, end_time=endDate)

                    # no history for this time period
                    if not history:
                        self.Log(
                            f"no history provided for days: {startDayPeriod}/{endDayPeriod}", E_WARNING)
                        break

                    # if this is a single day, the history is not array
                    if len(history) > 0:
                        history = history[0]

                    # append all to historys
                    baseswitch_historys = baseswitch_historys + history

            break

            # cycle baseswitch history events
            self.Log(
                f"history data to analyze: {len(baseswitch_historys)}", E_INFO)

            # set and reset the counter of merged time period
            countMergeTimePeriod = {
                0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

            # set and reset the maximum value of baseSwitch status event
            # << temp. disabled >>
            # maxBaseSwitchCountEvents = 0

            for baseSwitchHistory in baseswitch_historys:

                ###############################################################
                # BASE SWITCH ROUTINE
                ###############################################################

                # get and convert the hystory Date
                historyDate = utility.convertdatatime(
                    baseSwitchHistory['last_changed'])

                # set a variable with the date rounded by config value
                historyDateRounded = (historyDate - datetime.timedelta(
                    minutes=historyDate.minute % config.Get('roundtimeevents')))

                # set a variable with this state of baseSwitch
                baseSwitchHistoryState = baseSwitchHistory['state']

                # set the weekDay object if not already setted
                entityStates['bt'] = utility.setifnotexist(
                    entityStates['bt'], 'periodon', {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []})

                # if the state are ON and we are not already onStatePeriod (on-off)
                if baseSwitchHistoryState == "on" and isOnStatePeriod['state'] == False:

                    # set this is a OnStatePeriod
                    isOnStatePeriod['state'] = True

                    # set the date
                    isOnStatePeriod['datetime'] = historyDateRounded.strftime(
                        ONPERIOD_DATETIME_FORMAT)

                # if the state are OFF and we are in onStatePeriod (on-off)
                if baseSwitchHistoryState == "off" and isOnStatePeriod['state'] == True:

                    # merge this period if are the same or similar by config
                    if entityStates['bt']['periodon'][historyDate.weekday()]:

                        # set the Count of array
                        kCount = 0

                        # set the found to merge boolean
                        foundMerge = False

                        # cycle all period for search similarity
                        for isOnData in entityStates['bt']['periodon'][historyDate.weekday()]:

                            # calculate difference with ON time
                            onDateTimeDiffMin = int((_datetime.strptime(
                                isOnData['on'], "%H:%M") - _datetime.strptime(isOnStatePeriod['datetime'], "%H:%M")).total_seconds()/60)

                            # calculate difference with OFF time
                            offDateTimeDiffMin = int((_datetime.strptime(
                                isOnData['off'], "%H:%M")-historyDateRounded.replace(
                                year=1900, month=1, day=1, second=0)).total_seconds()/60)

                            # if absolute value of difference are below of config value and are greaters than 0
                            if abs(onDateTimeDiffMin) < config.Get('mergeonperiodminutes'):

                                # replace the ON time
                                entityStates['bt']['periodon'][historyDate.weekday(
                                )][kCount]['on'] = isOnStatePeriod['datetime']

                                # increment the counter
                                entityStates['bt']['periodon'][historyDate.weekday(
                                )][kCount]['count'] += 1

                                # set the found to merge boolean True
                                foundMerge = True

                                # increment the mergedTimePeriod counter
                                countMergeTimePeriod[historyDate.weekday(
                                )] += 1

                                # logging
                                self.Log(
                                    f"merged ON period wD{historyDate.weekday()}: {isOnData['on']} with {isOnStatePeriod['datetime']} (count:{len(entityStates['bt']['periodon'][historyDate.weekday()])})", E_DEBUG)

                            # if absolute value of difference are below of config value and are greaters than 0
                            if abs(offDateTimeDiffMin) < config.Get('mergeonperiodminutes'):

                                # replace the OFF time
                                entityStates['bt']['periodon'][historyDate.weekday(
                                )][kCount]['off'] = historyDateRounded.strftime(ONPERIOD_DATETIME_FORMAT)

                                # set the found to merge boolean True
                                foundMerge = True

                                # increment the mergedTimePeriod counter
                                countMergeTimePeriod[historyDate.weekday(
                                )] += 1

                                # logging
                                self.Log(
                                    f"merged OFF period wD{historyDate.weekday()}: {isOnData['off']} with {historyDateRounded.strftime(ONPERIOD_DATETIME_FORMAT)} (count:{len(entityStates['bt']['periodon'][historyDate.weekday()])})", E_DEBUG)

                            # if entityStates['bt']['periodon'][historyDate.weekday(
                            # )][k]['count'] > maxBaseSwitchCountEvents:
                            #     maxBaseSwitchCountEvents = entityStates['bt']['periodon'][historyDate.weekday(
                            #     )][k]['count']

                            # increment counter
                            kCount += 1

                        if not foundMerge:

                            # if not found to merge, simply append as new
                            entityStates['bt']['periodon'][historyDate.weekday()].append(
                                {"on": isOnStatePeriod['datetime'],
                                 "off": historyDateRounded.strftime(ONPERIOD_DATETIME_FORMAT),
                                 "count": 1
                                 })

                    else:

                        # if not found to merge, simply append as new
                        entityStates['bt']['periodon'][historyDate.weekday()].append(
                            {"on": isOnStatePeriod['datetime'],
                                "off": historyDateRounded.strftime(ONPERIOD_DATETIME_FORMAT),
                                "count": 1
                             })

                    # reset OnStatePeriod
                    isOnStatePeriod['state'] = False

                ###############################################################
                # BASED ON ENTITIES ROUTINE
                ###############################################################
                # cycle of all basedOn Entities
                for basedonEntity in config.Get(['predictsevent', event, 'basedon']):

                    # calculate period from time by config to switchBase changed event
                    startHistory = historyDate - \
                        datetime.timedelta(seconds=config.Get(
                            'timerangehistoryseconds'))
                    endHistory = historyDate + \
                        datetime.timedelta(seconds=config.Get(
                            'timerangehistoryseconds'))

                    # logging
                    self.Log(
                        f"history: {basedonEntity} from {startHistory} for {config.Get('timerangehistoryseconds')} sec", E_DEBUG)

                    # ask history
                    basedOnEntityHistorys = self.get_history(
                        entity_id=basedonEntity, end_time=endHistory, start_time=startHistory)

                    # check if exist
                    if basedOnEntityHistorys:

                        # logging
                        self.Log(
                            f"get {len(basedOnEntityHistorys[0])} history items", E_DEBUG)

                        # init object if is'nt inited
                        entityStates['bo'] = utility.setifnotexist(
                            entityStates['bo'], basedonEntity, {'type': None})

                        # cycle of basedOn entity history
                        for basedOnEntityHistory in basedOnEntityHistorys[0]:

                            # get state
                            state = basedOnEntityHistory['state']

                            if state in ['on', 'off'] or isinstance(state, str) and not utility.stringisnumber(state):
                                ############################################################
                                # BASEDONENTITY STATE ARE BOOLEAN OR STRING
                                ############################################################

                                # set the type for futhure use
                                entityStates['bo'][basedonEntity]['type'] = "string"

                                # init the object if is'nt initied
                                entityStates['bo'][basedonEntity] = utility.setifnotexist(
                                    entityStates['bo'][basedonEntity], state, {'count': 0, 'probs': 0})

                                # increment value of this state hits
                                entityStates['bo'][basedonEntity][state]['count'] += 1

                                # calculate the probability
                                # (count of this state * 100)/lenght of history of base switchg
                                entityStates['bo'][basedonEntity][state]['probs'] = round((
                                    entityStates['bo'][basedonEntity][state]['count'] * 100)/len(baseswitch_historys), 2)

                            if utility.stringisnumber(state):
                                ############################################################
                                # BASEDONENTITY STATE ARE INTEGER OR FLOAT
                                ###########################################################

                                # set the type for futhure use
                                entityStates['bo'][basedonEntity]['type'] = "float"

                                # get numerico state
                                valueState = float(state)

                                # set averageObject if aren't setted
                                averageObject = utility.setifnotexist(
                                    averageObject, basedonEntity, [])

                                # append the valueState (numeric)
                                averageObject[basedonEntity].append(valueState)

                                # init the object with min/max/average key if is'nt inited
                                entityStates['bo'][basedonEntity] = utility.setifnotexist(
                                    entityStates['bo'][basedonEntity], 'min', valueState)
                                entityStates['bo'][basedonEntity] = utility.setifnotexist(
                                    entityStates['bo'][basedonEntity], 'max', valueState)
                                entityStates['bo'][basedonEntity] = utility.setifnotexist(
                                    entityStates['bo'][basedonEntity], 'average', valueState)

                                # calculate the min, the max and the average
                                if valueState < entityStates['bo'][basedonEntity]['min']:
                                    entityStates['bo'][basedonEntity]['min'] = valueState
                                if valueState > entityStates['bo'][basedonEntity]['max']:
                                    entityStates['bo'][basedonEntity]['max'] = valueState
                                entityStates['bo'][basedonEntity]['average'] = round(0 if len(
                                    averageObject[basedonEntity]) == 0 else sum(averageObject[basedonEntity])/len(averageObject[basedonEntity]), 2)

            # # filters the BaseSwitch periodOn data by excluding insignificant events
            # for weekday in range(0, len(countMergeTimePeriod.keys())):
            #     if weekday in entityStates['bt']['periodon']:
            #         entityStates['bt']['periodon'][weekday] = [d for d in entityStates['bt']['periodon']
            #                                                    [weekday] if d['count'] <= int((d['count']*100)/maxBaseSwitchCountEvents)]

            # add startdate and enddate to entityStates
            entityStates['updatedate'] = [
                eventsHistoryStartDate.strftime(DATETIME_FORMAT), eventsHistoryEndDate.strftime(DATETIME_FORMAT)]

            # convert to json and write on file
            fileEventSave = open(os.path.join(_currentfolder,
                                              MODELPATH, f"{event}.json"), "w")
            fileEventSave.write(json.dumps(entityStates))
            fileEventSave.close()

            # logging
            self.Log(f"model for <{event}> saved", E_INFO)
