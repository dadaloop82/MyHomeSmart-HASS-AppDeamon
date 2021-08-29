import hassapi as hass
import datetime
from dateutil import tz
import re


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
                datatimeString = datetime.datetime.strptime(
                    datatimeString, ALT_DATETIME_FORMAT).strftime(DATETIME_FORMAT)
            a = self._hass.parse_utc_string(datatimeString)
            b = datetime.datetime.utcfromtimestamp(a)
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

        config = self.Config(self)
        utility = self.Utility(self)
        self.TIMEZONE = tz.gettz(config.Get("timezone"))

        # getting predict's event
        # bt = baseentity
        # bo = basedOnEntities
        entityStates = {'bt': {}, 'bo': {}}
        baseswitch_historys = []
        averageObject = {}
        isOnState = {'state': False, 'datetime': None}

        for event in config.Get('predictsevent'):
            # get baseswitch
            baseswitch = config.Get(['predictsevent', event, 'basewitch'])
            # get history of baseswitch
            self.Log(f"ask baseSwitch: {baseswitch} history ", E_DEBUG)

            if(config.Get('historyday') > 10):
                # for more 10 days
                currentDate = datetime.datetime.now()
                cycle = int(config.Get('historyday')/10)+1
                for number in range(0, cycle):
                    startDayPeriod = number*10
                    endDayPeriod = startDayPeriod+10
                    if endDayPeriod > config.Get('historyday'):
                        endDayPeriod = config.Get('historyday')

                    # calculate date
                    endDate = utility.getdifferncedate(
                        currentDate.replace(hour=23, minute=59), "days", startDayPeriod)
                    startDate = utility.getdifferncedate(
                        currentDate.replace(hour=00, minute=00), "days", endDayPeriod)

                    # get history
                    self.Log(
                        f"parsing and analyze history data (days: {startDayPeriod}/{endDayPeriod})", E_INFO)
                    history = self.get_history(
                        entity_id=baseswitch, start_time=startDate, end_time=endDate)
                    if len(history) > 0:
                        history = history[0]
                    baseswitch_historys = baseswitch_historys + history

            else:
                # for max 10 days
                self.Log(f"parsing and analyze history data (1 cycle)", E_INFO)
                baseswitch_historys = self.get_history(
                    entity_id=baseswitch, days=config.Get('historyday'))[0]

            # cycle baseswitch history events
            self.Log(
                f"history data to analyze: {len(baseswitch_historys)}", E_INFO)
            countMergeTimePeriod = {
                0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
            for baseSwitchHistory in baseswitch_historys:

                ###############################################################
                # BASE SWITCH ROUTINE
                ###############################################################

                historyDate = utility.convertdatatime(
                    baseSwitchHistory['last_changed'])
                historyDateRounded = (historyDate - datetime.timedelta(
                    minutes=historyDate.minute % config.Get('roundtimeevents')))
                baseSwitchHistoryState = baseSwitchHistory['state']

                # calculate period for state ON
                if not 'periodon' in entityStates['bt']:
                    # weekday (0-6)
                    entityStates['bt']['periodon'] = {
                        0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []}

                if baseSwitchHistoryState == "on" and isOnState['state'] == False:
                    isOnState['state'] = True
                    isOnState['datetime'] = historyDateRounded.strftime(
                        ONPERIOD_DATETIME_FORMAT)

                if baseSwitchHistoryState == "off" and isOnState['state'] == True:

                    # group by similar hour
                    if entityStates['bt']['periodon'][historyDate.weekday()]:
                        k = 0
                        foundMerge = False
                        for isOnData in entityStates['bt']['periodon'][historyDate.weekday()]:

                            onDateTimeDiffMin = int((datetime.datetime.strptime(
                                isOnData['on'], "%H:%M") - datetime.datetime.strptime(isOnState['datetime'], "%H:%M")).total_seconds()/60)

                            offDateTimeDiffMin = int((datetime.datetime.strptime(
                                isOnData['off'], "%H:%M")-historyDateRounded.replace(
                                year=1900, month=1, day=1, second=0)).total_seconds()/60)

                            if abs(onDateTimeDiffMin) < config.Get('mergeonperiodminutes') and onDateTimeDiffMin >= 0:

                                entityStates['bt']['periodon'][historyDate.weekday(
                                )][k]['on'] = isOnState['datetime']
                                entityStates['bt']['periodon'][historyDate.weekday(
                                )][k]['count'] += 1
                                foundMerge = True
                                countMergeTimePeriod[historyDate.weekday(
                                )] += 1
                                self.Log(
                                    f"merged: { countMergeTimePeriod[historyDate.weekday()]} ON period's in WD {historyDate.weekday()} in range {config.Get('mergeonperiodminutes')}min rounded by {config.Get('roundtimeevents')}min", E_DEBUG)

                            if abs(offDateTimeDiffMin) < config.Get('mergeonperiodminutes') and offDateTimeDiffMin <= 0:
                                entityStates['bt']['periodon'][historyDate.weekday(
                                )][k]['off'] = historyDateRounded.strftime(ONPERIOD_DATETIME_FORMAT)
                                foundMerge = True
                                countMergeTimePeriod[historyDate.weekday(
                                )] += 1
                                self.Log(
                                    f"merged: { countMergeTimePeriod[historyDate.weekday()]} OFF period's in WD {historyDate.weekday()} in range {config.Get('mergeonperiodminutes')}min round by {config.Get('roundtimeevents')}min", E_DEBUG)
                            k += 1

                        if not foundMerge:
                            entityStates['bt']['periodon'][historyDate.weekday()].append(
                                {"on": isOnState['datetime'],
                                 "off": historyDateRounded.strftime(ONPERIOD_DATETIME_FORMAT),
                                 "count": 1
                                 })

                    else:
                        entityStates['bt']['periodon'][historyDate.weekday()].append(
                            {"on": isOnState['datetime'],
                                "off": historyDateRounded.strftime(ONPERIOD_DATETIME_FORMAT),
                                "count": 1
                             })

                    isOnState['state'] = False

                ###############################################################
                # BASED ON ENTITIES ROUTINE
                ###############################################################

                for basedonEntity in config.Get(['predictsevent', event, 'basedon']):
                    # get entity history from period
                    st = historyDate - \
                        datetime.timedelta(seconds=config.Get(
                            'timerangehistoryseconds'))
                    et = historyDate + \
                        datetime.timedelta(seconds=config.Get(
                            'timerangehistoryseconds'))
                    self.Log(
                        f"history: {basedonEntity} from {st} for {config.Get('timerangehistoryseconds')} sec", E_DEBUG)
                    BasedOnEntityHistorys = self.get_history(
                        entity_id=basedonEntity, end_time=et, start_time=st)
                    if BasedOnEntityHistorys:
                        self.Log(
                            f"get {len(BasedOnEntityHistorys[0])} history items", E_DEBUG)

                        # are avaibile a history for this period
                        if not basedonEntity in entityStates['bo']:
                            # define a entitystates for this basedon_entity
                            entityStates['bo'][basedonEntity] = {}

                        for entity_history in BasedOnEntityHistorys[0]:
                            state = entity_history['state']

                            if state in ['on', 'off'] or isinstance(state, str) and not utility.stringisnumber(state):
                                ############################################################
                                # BASEDONENTITY STATE ARE BOOLEAN OR STRING
                                ############################################################
                                entityStates['bo'][basedonEntity]['type'] = "string"
                                if not state in entityStates['bo'][basedonEntity]:
                                    # define a entitystates for this state
                                    entityStates['bo'][basedonEntity][state] = {
                                        'count': 0, 'probs': 0}
                                # increment value
                                entityStates['bo'][basedonEntity][state]['count'] += 1
                                entityStates['bo'][basedonEntity][state]['probs'] = round((
                                    entityStates['bo'][basedonEntity][state]['count'] * 100)/len(baseswitch_historys), 2)

                            if utility.stringisnumber(state):
                                ############################################################
                                # BASEDONENTITY STATE ARE INTEGER OR FLOAT
                                ###########################################################
                                entityStates['bo'][basedonEntity]['type'] = "float"
                                valueState = float(state)
                                if not basedonEntity in averageObject:
                                    averageObject[basedonEntity] = []
                                averageObject[basedonEntity].append(valueState)

                                if not 'min' in entityStates['bo'][basedonEntity]:
                                    # define a entitystates for this state
                                    entityStates['bo'][basedonEntity] = {
                                        'min': valueState, 'max': valueState, 'average': valueState}
                                else:
                                    if valueState < entityStates['bo'][basedonEntity]['min']:
                                        entityStates['bo'][basedonEntity]['min'] = valueState
                                    if valueState > entityStates['bo'][basedonEntity]['max']:
                                        entityStates['bo'][basedonEntity]['max'] = valueState
                                    entityStates['bo'][basedonEntity]['average'] = round(0 if len(
                                        averageObject[basedonEntity]) == 0 else sum(averageObject[basedonEntity])/len(averageObject[basedonEntity]), 2)

        # analyze data and create model
        self.Log(entityStates)
