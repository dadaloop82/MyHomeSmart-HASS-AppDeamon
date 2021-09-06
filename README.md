# Home Assistant - Power with your control!

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/dadaloop82)

### **WORK IN PROGRESS - CURRENTLY NOT COMPLETE AND NOT WORK**
### This is an idea under development (when I have free time)
#### *I am Italian, sorry for any mistakes in English.*


# I have a dream: make my life smarter!
Based on the analysis of the change of a certain switch (set in configuration), the system analyzes the change of the sensors in that moment
So it creates a model, divided by periods (including seasons, etc. ..) trying to guess their habits and if the conditions are similar, it proposes via Alexa the activation of the switch, learning from the answers given.
If the probability of activation is very high, the action could be performed automatically without any iteration with the user.

# Ingredients:
- Working instance of **Home Assistant** (https://www.home-assistant.io/)
- Working addon **appDeamon** for HASS (https://github.com/AppDaemon/appdaemon)
- Optional **influxDB database** - otherwise takes data from **HASS history** (they are limited!)
- A minimal knowledge of Python and how appDeamon works

# Use case example

- On work days, you normally watch the news on television after coffee. After gaining enough experience from your history and habits, Alexa will ask if you enjoy watching television, or HomeAssistant will automatically turn it on if the probability is very high.

- When it's hot, you normally turn on the air conditioner and some times you forget the windows are open. Alexa may ask you to close the windows because it would be time to turn on the air conditioner, or it may do it automatically as it has enough experience.

- When no one is home, HASS can interactively or automatically perform certain actions you normally do, such as activating the robot vacuum or turning on the house alarm

Warning: all these automatic automations are based on actions already performed previously, according to probabilistic calculations. 

**It is not foreseen that the system considers to ask or to execute actions in a completely spontaneous way.**



## Want to help? You are welcome!
This is and shall be an open, free and non-profit project; the goal is to create an automated system to manage situations in HomeAssistant.

Or, if you want to thank me for what I do by buying me a coffee:

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/dadaloop82)

**No one should and will ever make money from this project**.

If you want to help me in any way (advice, code, etc...) you are welcome to do so and I really thank you very much!
Use the tools that Github provides!


