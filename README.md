# Home Assistant AppDeamon  - Event predictor

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/dadaloop82)

### **WORK IN PROGRESS - CURRENTLY NOT COMPLETE AND NOT WORK**
### This is an idea under development (when I have free time)
#### *I am Italian, sorry for any mistakes in English.*

# I want to try it right now!
**No, wait.**

This is a program in Python that I'm making in my spare time and is currently unfinished.

To try it and possibly contribute (thanks!) these are the ingredients:

- knowledge of Python

- a working instance of Home Assistant
- the appDeamon addon correctly installed and running 

# The idea (and the dream)
My goal (and dream) is for Home Assistant to decide autonomously when it is appropriate to activate a certain event, based on the history of one or more switches, relating the date and time and the status of other sensors.
Based on the calculations performed, if the level of certainty is high it could directly activate the switch, or if it is low (uncertain) it could ask through Alexa (Amazon) if you want to proceed with the activation and based on the answer given it could even modify its data model.

# Use case example

- An automation is automatically created to start the robot vacuum cleaner when nobody is at home, the time slot is from 14:00 to 18:00, the balcony door is closed and the humidity is below 60%.

- An automation is automatically created to turn on the television when someone is at home, it is between 20:00 and 22:00, dinner is being served, the temperature in the house is above 22°C and there is no upcoming appointment on the calendar.

- Asked if you want coffee if the time slot is from 12:00 to 14:00, someone is at home, you have just finished having lunch, the temperature at home is below 25°C - if not, the model is modified 

Warning: all these automatic automations are based on actions already performed previously, according to probabilistic calculations. 

**It is not foreseen that the system considers to ask or to execute actions in a completely spontaneous way.**

# Progress & ToDo

- [x] (OP #1) Getting the history of a specific switch in specified time period 
- [x] (OP #2) Getting the history of all connected sensors 
- [x] Caching the history
- [x] (OP #4) get time slot from the history of the based on sensors
- [x] (OP #5) Filters the BaseSwitch periodOn data by excluding insignificant events
- [x] (OP #7) Save the model (and reuse for caching)
- [ ] (OP #8) Listen of variation on baseOnSensor
- [ ] (OP #9) Send an event to Home Assistant with the potential switch

- [x] (Thanks [@Pirol62](https://github.com/dadaloop82/HASS_AppDeamon_SwitchPredictor/issues/1)) consider the variation of time  (season, year, ecc...)

- [ ] Optimizing Code
- [ ] Testing
- [ ] more Testing :)

# Operation diagram

1. Getting the history of a specific switch (*baseSwitch*) in specified time period (by config)

2. Getting the history of all connected sensors (*basedOnSensor* - declared on Config) in the time interval in which baseSwitch has been activated (on) since a time specified in configuration
3. Now I have the real situation (snapshot) of what has changed before the *baseSwitch* was activated
4. From the history of the various sensors (*basedOnSensor*), when they change state, group the times by rounding them to a value specified in the configuration, thus obtaining the day of the week, the hour, the minutes of the event and calculate the frequency of repetition
5. Discard the data that are not satisfactory or because they are too few (by config)
6. Now have an overview of what triggered *basedOnSensor* to turn on, with the relevant time periods broken down by days of the week
7. Save the model
8. Listen to the variations of the *basedOnSensor* and compare them with the results of the model
9. Send an event to Home Assistant with the potential switch to manage the probability of it happening. It will be in Home Assistant that will decide what to do, whether to activate the switch or ask the user if they want to activate it.

## Want to help? You are welcome!
This is and shall be an open, free and non-profit project; the goal is to create an automated system to manage situations in HomeAssistant.

Or, if you want to thank me for what I do by buying me a coffee:

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/dadaloop82)

**No one should and will ever make money from this project**.

If you want to help me in any way (advice, code, etc...) you are welcome to do so and I really thank you very much!
Use the tools that Github provides!


