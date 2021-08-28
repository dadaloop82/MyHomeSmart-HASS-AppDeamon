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
                        currentDate, "days", startDayPeriod)
                    startDate = utility.getdifferncedate(
                        currentDate, "days", endDayPeriod)

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
            for historyData in baseswitch_historys:
                historyDate = utility.convertdatatime(
                    historyData['last_changed'])
                historyState = historyData['state']

                # w=weekday|d=day|m=month|h=hour|i=minutes
                dtcomponents = [
                    {'w': historyDate.weekday()},
                    {'d': historyDate.day},
                    {'m': historyDate.month},
                    {'h': historyDate.hour},
                    {'i': historyDate.minute}
                ]

                for dtcomponent in dtcomponents:
                    k, v = list(dtcomponent.items())[0]

                    if not historyState in entityStates['bt']:
                        entityStates['bt'][historyState] = {}
                    if not k in entityStates['bt'][historyState]:
                        # m=min|x=max
                        entityStates['bt'][historyState][k] = {
                            'm': 999, 'x': 0}

                    if v < entityStates['bt'][historyState][k]['m']:
                        entityStates['bt'][historyState][k]['m'] = v
                    if v > entityStates['bt'][historyState][k]['x']:
                        entityStates['bt'][historyState][k]['x'] = v

                # cycle basedon entities
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
                        # entityStates = {}

                        if not basedonEntity in entityStates['bo']:
                            # define a entitystates for this basedon_entity
                            entityStates['bo'][basedonEntity] = {}

                        for entity_history in BasedOnEntityHistorys[0]:
                            state = entity_history['state']
                            if not state in entityStates['bo'][basedonEntity]:
                                # define a entitystates for this state
                                entityStates['bo'][basedonEntity][state] = {
                                    'count': 0, 'probs': 0}
                            # increment value
                            entityStates['bo'][basedonEntity][state]['count'] += 1
                            entityStates['bo'][basedonEntity][state]['probs'] = round((
                                entityStates['bo'][basedonEntity][state]['count'] * 100)/len(baseswitch_historys), 2)

        # analyze data and create model
        self.Log(entityStates)
