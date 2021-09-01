import hassapi as hass
import datetime
import time
import os
import json
import hashlib

from dateutil import tz
from os.path import exists


# Constant
#E_DEBUG = "INFO"
E_DEBUG = "DEBUG"
E_INFO = "INFO"
E_WARNING = "WARNING"
E_ERROR = "ERROR"

CONST_HEMISPHERE = "north"

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

        def roundDateByMinutes(self, dt, delta):
            return (dt + (datetime.datetime.min - dt) % delta).replace(year=1900, month=1, day=1, second=0, microsecond=00)

        def getSeasonByDate(self, date):
            md = date.month * 100 + date.day
            if ((md > 320) and (md < 621)):
                s = 0  # spring
            elif ((md > 620) and (md < 923)):
                s = 1  # summer
            elif ((md > 922) and (md < 1223)):
                s = 2  # fall
            else:
                s = 3  # winter
            if not CONST_HEMISPHERE == 'north':
                s = (s + 2) % 3
            return s

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
        entityStates = {'bt': {'periodon': []}, 'bo': {}}
        baseswitch_historys = []
        averageObject = {}
        OnStatePeriod = {'start': None, 'end': None}
        isDataLoadedFromFile = False
        dayHistoryPeriod = config.Get('historyday')
        firstDateWithNoHistory = _currentDate

        for event in config.Get('predictsevent'):

            # get baseswitch
            baseswitch = config.Get(['predictsevent', event, 'basewitch'])

            # set configHash
            configHash = [baseswitch, config.Get(
                ['predictsevent', event, 'basedon'])]
            configHashMd5 = hashlib.md5(
                ''.join(map(str, configHash)).encode('utf-8')).hexdigest()

            # check if model is already saved
            fileName = os.path.join(_currentfolder, MODELPATH, f"{event}.json")

            if exists(fileName):

                # if the file exist, read the json data (model)
                self.Log(f"{event}: model already exist - load and use them ")
                fileEventCached = open(fileName,)

                # put the data on entityStates variable
                entityStatesTmp = json.load(fileEventCached)

                if entityStatesTmp and 'confighash' in entityStatesTmp and entityStatesTmp['confighash'] == configHashMd5:
                    # set the savedModelEventsHistoryStartDate|EndDate and the flag in isDataLoadedFromFile
                    entityStates = entityStatesTmp
                    savedModelEventsHistoryEndDate = _datetime.strptime(
                        entityStates['updatedate'][0], DATETIME_FORMAT)
                    savedModelEventsHistoryStartDate = _datetime.strptime(
                        entityStates['updatedate'][1], DATETIME_FORMAT)
                    isDataLoadedFromFile = True
                else:
                    self.Log(
                        f"{event}: model file are not valid or config are changed", E_WARNING)

                fileEventCached.close()

            # get history of baseswitch
            self.Log(f"ask baseSwitch: {baseswitch} history ", E_DEBUG)

            # calculate che number of cycles
            cycle = int(dayHistoryPeriod/10)+1

            # start cycle
            for number in range(0, cycle):

                # calculate start and end period
                startDayPeriod = number*10
                endDayPeriod = startDayPeriod+10

                # if exceed, get the value in config
                if endDayPeriod > dayHistoryPeriod:
                    endDayPeriod = dayHistoryPeriod

                # calculate date
                endDate = utility.getdifferncedate(
                    _currentDate.replace(hour=23, minute=59, second=00, microsecond=00), "days", startDayPeriod)
                startDate = utility.getdifferncedate(
                    _currentDate.replace(hour=23, minute=59, second=00, microsecond=00), "days", endDayPeriod)

                if endDate > _currentDate:
                    endDate = _currentDate.replace(second=00, microsecond=00)

                if isDataLoadedFromFile:
                    self.Log(
                        f"{event}: Date requested: {startDate} - {endDate}", E_DEBUG)
                    self.Log(
                        f"{event}: Date cached:  {startDate} - {endDate}", E_DEBUG)

                # if is file loaded, check if the startDate are NOT between the already laoaded data
                if(isDataLoadedFromFile and startDate >= savedModelEventsHistoryStartDate):
                    startDate = savedModelEventsHistoryEndDate

                    self.Log(
                        f"{event}: Date calculated: {savedModelEventsHistoryStartDate} - {savedModelEventsHistoryEndDate}", E_DEBUG)

                # check if startDate is greater than enDate -> the data must be loaded from file
                if startDate >= endDate or (endDate-startDate).days == 0:
                    self.Log(
                        f"{event}: load data from cache: {startDayPeriod}/{endDayPeriod}", E_INFO)

                else:
                    # get history for this timeslot
                    self.Log(
                        f"{event}: ask history data for day {startDayPeriod}/{endDayPeriod} )", E_INFO)

                    history = self.get_history(
                        entity_id=baseswitch, start_time=startDate, end_time=endDate)

                    # no history for this time period
                    if not history:
                        self.Log(
                            f"{event}: no history provided from {startDayPeriod} days ago", E_WARNING)
                        if not firstDateWithNoHistory:
                            firstDateWithNoHistory = endDate
                        break

                    # if this is a single day, the history is not array
                    if len(history) > 0:
                        history = history[0]

                    # append all to historys
                    baseswitch_historys = baseswitch_historys + history

            # cycle baseswitch history events
            if not isDataLoadedFromFile:
                self.Log(
                    f"{event}: history data to analyze NEW: {len(baseswitch_historys)}", E_INFO)
            elif len(baseswitch_historys):
                self.Log(
                    f"{event}: history data to analyze UPDATE: {len(baseswitch_historys)}", E_INFO)

            # set updatetime
            entityStates['updatedate'] = [
                _currentDate.strftime(DATETIME_FORMAT),
                (endDate if firstDateWithNoHistory else firstDateWithNoHistory).replace(
                    hour=00, minute=00, second=00, microsecond=00).strftime(DATETIME_FORMAT)
            ]

            # set configHash
            configHash = [baseswitch, config.Get(
                ['predictsevent', event, 'basedon'])]
            entityStates['confighash'] = configHashMd5

            startAnalyzingTime = time.time()
            countMergedOnTimeSlot = 0
            isThisOnPeriod = False
            for baseSwitchHistory in baseswitch_historys:

                ###############################################################
                # BASE SWITCH ROUTINE
                # - TIME SLOT CALCULATION
                #   array structure
                #   [0] = count
                #   [1] = startTime
                #   [2] = endTime
                #   [3] = weekday (0-6)
                #   [4] = season (0-3)
                ###############################################################

                # get and convert the hystory Date
                historyDate = utility.convertdatatime(
                    baseSwitchHistory['last_changed'])

                # set a variable with the date rounded by config value
                historyTimeRounded = utility.roundDateByMinutes(
                    historyDate, datetime.timedelta(minutes=config.Get('roundtimeevents')))

                # set a variable with this state of baseSwitch
                baseSwitchHistoryState = baseSwitchHistory['state']

                # if the state are ON and we are not already onStatePeriod (on-off)
                if baseSwitchHistoryState == "on" and not isThisOnPeriod:
                    # PERIOD ON START
                    isThisOnPeriod = True
                    OnStatePeriod['start'] = historyTimeRounded

                elif baseSwitchHistoryState == "off" and isThisOnPeriod:
                    # PERIOD ON END
                    isThisOnPeriod = False
                    OnStatePeriod['end'] = historyTimeRounded

                    # check for period's merge
                    k = 0
                    merged = False
                    for periodOn in entityStates['bt']['periodon']:

                        if periodOn[3] != historyDate.weekday() and periodOn[4] != utility.getSeasonByDate(historyDate) and OnStatePeriod['start'] == OnStatePeriod['end']:
                            k += 1
                            continue

                        timePeriod = [_datetime.strptime(
                            periodOn[1], "%H:%M"), _datetime.strptime(periodOn[2], "%H:%M")]

                        diffStart = int(
                            (timePeriod[0] - OnStatePeriod['start']).total_seconds()/60)
                        diffEnd = int(
                            (timePeriod[1] - OnStatePeriod['end']).total_seconds()/60)

                        if abs(diffStart) < config.Get('mergeonperiodminutes'):
                            entityStates['bt']['periodon'][k][1] = OnStatePeriod['start'].strftime(
                                ONPERIOD_DATETIME_FORMAT)
                            merged = True

                        if abs(diffEnd) < config.Get('mergeonperiodminutes'):
                            entityStates['bt']['periodon'][k][2] = OnStatePeriod['end'].strftime(
                                ONPERIOD_DATETIME_FORMAT)
                            merged = True

                        if merged:
                            entityStates['bt']['periodon'][k][0] += 1

                        k += 1

                    # save period on array
                    if not merged:
                        entityStates['bt']['periodon'].append(
                            [
                                # count
                                0,
                                # start time
                                OnStatePeriod['start'].strftime(
                                    ONPERIOD_DATETIME_FORMAT),
                                # end time
                                OnStatePeriod['end'].strftime(
                                    ONPERIOD_DATETIME_FORMAT),
                                # weekday (0-6)
                                historyDate.weekday(),
                                # season
                                utility.getSeasonByDate(OnStatePeriod['end'])
                            ]
                        )
                    else:
                        countMergedOnTimeSlot += 1

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
                                    entityStates['bo'][basedonEntity], state, {'count': 0})

                                # increment value of this state hits
                                entityStates['bo'][basedonEntity][state]['count'] += 1

                                # calculate the probability
                                # (count of this state * 100)/lenght of history of base switchg
                                # entityStates['bo'][basedonEntity][state]['probs'] = round((
                                #     entityStates['bo'][basedonEntity][state]['count'] * 100)/len(baseswitch_historys), 2)

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
                                entityStates['bo'][basedonEntity] = utility.setifnotexist(
                                    entityStates['bo'][basedonEntity], 'count', 0)

                                # calculate the min, the max and the average
                                if valueState < entityStates['bo'][basedonEntity]['min']:
                                    entityStates['bo'][basedonEntity]['min'] = valueState
                                if valueState > entityStates['bo'][basedonEntity]['max']:
                                    entityStates['bo'][basedonEntity]['max'] = valueState
                                entityStates['bo'][basedonEntity]['count'] += 1
                                entityStates['bo'][basedonEntity]['average'] = round((
                                    entityStates['bo'][basedonEntity]['min']+entityStates['bo'][basedonEntity]['max'])/2, 2)
            if countMergedOnTimeSlot:
                self.Log(
                    f"{event}: merged {countMergedOnTimeSlot} ON timeslot ", E_INFO)

            # if len(baseswitch_historys):
            #     # convert to json and write on file
            #     fileEventSave = open(os.path.join(_currentfolder,
            #                                       MODELPATH, f"{event}.json"), "w")
            #     fileEventSave.write(json.dumps(entityStates))
            #     fileEventSave.close()

            #     if isDataLoadedFromFile:
            #         self.Log(f"{event}: model UPDATED", E_INFO)
            #     else:
            #         self.Log(f"{event}: model CREATED  ", E_INFO)

            print(entityStates)

            self.Log(
                f"{event}: analyzed model for in {round((time.time())-startAnalyzingTime,2)} sec.", E_INFO)
