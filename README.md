# Home Assistant - Power with your control!

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/dadaloop82)

## HASS + appDeamon + Pandas (+ influxDB)

# I have a dream: make my life smarter!
Based on the analysis of the change of a certain switch (set in configuration), the system analyzes the change of the sensors in that moment
So it creates a model, divided by periods (including seasons, etc. ..) trying to guess their habits and if the conditions are similar, it proposes via Alexa the activation of the switch, learning from the answers given.
If the probability of activation is very high, the action could be performed automatically without any iteration with the user.

### **WORK IN PROGRESS - CURRENTLY NOT COMPLETE AND NOT WORK**
### This is an idea under development (when I have free time)
#### *I am Italian, sorry for any mistakes in English.*


# Last news
* Code has been completely refactor and optimized, adding influxDB integration
* If the influxDB connection or instance should not exist, the program automatically relies on the built-in history of Home Assistant
* Pandas DataFrame is used for time management, and the following factors are considered, in addition to the date and time
  * Weekday
  * Season
  * Quarter
  * Beginning/end of the month
  * Week of Day
* Search for the situation that existed before the change and integrate it into the frame

# What's missing?

* Machine Learning approach (probabilistic scikit learn) for event prediction and model creation
* Event detection
* Probability management
* Management of the above events

# Ingredients:
- Working instance of **Home Assistant** (https://www.home-assistant.io/)
- Working addon **appDeamon** for HASS (https://github.com/AppDaemon/appdaemon)
- Dependencies installed in appdeamon (see dependencies section)
- Optional **influxDB database** - otherwise takes data from **HASS history** (they are limited!)
- A minimal knowledge of Python and how appDeamon works

# Dependencies 
*(specified in /appdeamon/config/apps/requirements.txt)*
- numpy (**installation are very slow, be patient!**)
- pandas (**installation are very slow, be patient!**)
- influxdb-client


# HomeAssistant build-in history or influxDB ?

It doesn't matter now.
It is possible to activate in the settings the reading from influxDB (with the configuration parameters in "secret.yaml") and read from a database with a very long data retention.
If this doesn't work or you don't have influxDB, the HomeAssistant history is automatically read, even if it is rather limited.

# Use case example

- On work days, you normally watch the news on television after coffee. After gaining enough experience from your history and habits, Alexa will ask if you enjoy watching television, or HomeAssistant will automatically turn it on if the probability is very high.

- When it's hot, you normally turn on the air conditioner and some times you forget the windows are open. Alexa may ask you to close the windows because it would be time to turn on the air conditioner, or it may do it automatically as it has enough experience.

- When no one is home, HASS can interactively or automatically perform certain actions you normally do, such as activating the robot vacuum or turning on the house alarm

Warning: all these automatic automations are based on actions already performed previously, according to probabilistic calculations. 

**It is not foreseen that the system considers to ask or to execute actions in a completely spontaneous way.**



# Want to help? You are welcome!
This is and shall be an open, free and non-profit project; the goal is to create an automated system to manage situations in HomeAssistant.

Or, if you want to thank me for what I do by buying me a coffee:

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/dadaloop82)

**No one should and will ever make money from this project**.

If you want to help me in any way (advice, code, etc...) you are welcome to do so and I really thank you very much!
Use the tools that Github provides!


