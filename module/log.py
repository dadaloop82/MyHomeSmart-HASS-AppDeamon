import inspect
import traceback
import module.constant as CONSTANT
# Variables


def LogError(_self, text, die=False):
    _self.log("--------------------------------------------------------")
    _self.error("[ ERROR ] in %s:%s \t\t %s" %
                (inspect.stack()[1][3], inspect.stack()[1][2], text))
    if die:
        _self.log("%s was terminated due to a fatal exception." %
                  (CONSTANT.APP_NAME))
        _self.log("--------------------------------------------------------")
        _self.log(traceback.format_exc())
        # exit()
    _self.log("--------------------------------------------------------")


def LogInfo(_self, text):
    _self.log(text)
