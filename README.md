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

## Want to help? You are welcome!
This is and shall be an open, free and non-profit project; the goal is to create an automated system to manage situations in HomeAssistant.

Or, if you want to thank me for what I do by buying me a coffee:

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/dadaloop82)

**No one should and will ever make money from this project**.

If you want to help me in any way (advice, code, etc...) you are welcome to do so and I really thank you very much!
Use the tools that Github provides!


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

# Features

- Calculation of the reason for activating the *baseSwitch*

- Calculation elements are the states of *basedOnSensor* that can be
    - Boolean
    - String
    - Value (in this case the minimum, the maximum and the average is computed) 

- Consider the variation of time in timeslot 
    - time
    - weekday
    - season

- Grouping of events into time slots and matching of similar time slots
    



# Data Model Structure
*(update at 01 September 2021)*



    bt = baseSwitch Time Slot
    bo = basedOnSensor state and calculated probability
    ['bt']['periodon]
      array structure
        [0] = count
        [1] = startTime
        [2] = endTime
        [3] = weekday (0-6)
        [4] = season (0-3)



example:

```
{'bt': {'periodon': [[1, '09:00', '09:15', 6, 3], [2, '17:15', '18:15', 6, 3], [0, '12:45', '13:30', 0, 3], [0, '18:45', '19:30', 0, 3], [0, '20:45', '22:15', 0, 3], [2, '12:30', '12:45', 1, 3], [1, '16:30', '21:45', 1, 3], [1, '16:30', '13:15', 2, 3], [0, '19:45', '20:00', 2, 3], [0, '20:45', '22:15', 2, 3], [0, '12:30', '12:45', 3, 3], [0, '18:30', '18:45', 3, 3], [0, '19:45', '20:30', 3, 3], [0, '20:45', '21:45', 3, 3], [1, '07:45', '07:45', 4, 3], [0, '11:45', '12:30', 4, 3], [0, '15:15', '18:15', 4, 3], [0, '09:30', '09:45', 5, 3], [0, '13:15', '13:45', 5, 3], [0, '21:00', '21:45', 5, 3], [0, '21:45', '22:15', 5, 3], [2, '09:45', '10:00', 6, 3], [2, '13:45', '14:00', 6, 3], [2, '18:45', '19:00', 6, 3], [2, '21:15', '21:45', 6, 3], [2, '22:30', '23:45', 6, 3], [0, '19:00', '21:15', 0, 3], [1, '07:30', '07:45', 1, 3], [1, '09:00', '11:00', 1, 3], [0, '19:30', '21:30', 1, 3], [2, '10:45', '09:00', 6, 3]]}, 'bo': {'person.daniel_2': {'type': 'string', 'home': {'count': 65}, 'not_home': {'count': 9}}, 'person.giuliana': {'type': 'string', 'home': {'count': 58}, 'not_home': {'count': 16}}, 'sensor.temperatura_e_umidita_temperature_measurement': {'type': 'float', 'min': 22.88, 'max': 25.62, 'average': 24.25, 'count': 74}, 'sensor.temperatura_e_umidita_relative_humidity_measurement': {'type': 'float', 'min': 38.0, 'max': 69.5, 'average': 53.75, 'count': 74}}, 'updatedate': ['2021-09-01T08:58:59+00:00', '2021-08-12T00:00:00+00:00']}
```
