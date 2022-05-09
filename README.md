<p align="center">
    <img src="https://repository-images.githubusercontent.com/400867168/04e42aaa-02dc-47f1-81b5-e6efde956004?sanitize=true"
        height="170">
</p>
<p align="center">
    <a alt="Stars">
        <img src="https://img.shields.io/github/stars/dadaloop82/MyHomeSmart-HASS-AppDeamon.svg" height="20px"/>
        </a>
    <a alt="Watcher">
        <img src="https://img.shields.io/github/watchers/dadaloop82/MyHomeSmart-HASS-AppDeamon.svg" height="20px"/>
    </a>
    <a alt="Followers">
        <img src="https://img.shields.io/github/followers/dadaloop82" height="20px"/>
    </a>
    <a alt="Issuses">
        <img src="https://img.shields.io/github/issues/dadaloop82/MyHomeSmart-HASS-AppDeamon.svg" height="20px" />
    </a>
    <br>         
      <a href="https://github.com/home-assistant/core" target="_blank" alt="Hass GitHub">Home assistant</a> 
      |
      <a href="https://github.com/AppDaemon/appdaemon" target="_blank" alt="AppDeamon GitHub">AppDeamon</a>
      |
      <a href="https://github.com/scikit-learn/scikit-learn" target="_blank" alt="SciKit GitHub">Scikit-learn (tree)</a>      
</p>


[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/dadaloop82)

[ Table of Content ]

- [1. This project is based on the following projects:](#1-this-project-is-based-on-the-following-projects)
- [2. What does mean "Give intelligence to Home automation"?](#2-what-does-mean-give-intelligence-to-home-automation)
- [3. What is the goal of this project?](#3-what-is-the-goal-of-this-project)
- [4. Can you give a simpler explanation?](#4-can-you-give-a-simpler-explanation)
- [5. The configuration file](#5-the-configuration-file)
- [6. How to install the script?](#6-how-to-install-the-script)


# 1. This project is based on the following projects:

- [thesillyhome-addon-repo](https://github.com/lcmchris/thesillyhome-addon-repo) by [lcmchris](https://github.com/lcmchris) (***Apache License 2.0***)

I sincerely thank these people for the great inspiration, ideas and information they have shared with me!


# 2. What does mean "Give intelligence to Home automation"?

Today we can enjoy several devices called "smart"; devices that seem to possess reasoning, logic and deduction skills in performing seemingly spontaneous actions.
In reality, this is not the case at all, each device is programmed to do actions under certain conditions, without any understanding of what it is doing and the possible consequence that such actions can do.
For example, smart speakers simply read what they find on the web, but they don't know if what they read is right or they cause the user to do the wrong thing.
A smart television is not smart, it just offers more opportunities for digital services.
And so on.

__Giving intelligence to home automation means giving a logical and comprehensive reasoning to the action that the home automation system should do to reach a certain objective.__

# 3. What is the goal of this project?

The goal of this project is to apply to [Home Assistant (HASS)](https://github.com/home-assistant) a system of automatic creation of dynamic automations able to activate or deactivate autonomously entities to achieve the prefixed purpose, whether it is dictated by the habits of the user or it is the right thing to do to achieve a certain purpose.
Home assistant already has the ability to manually create automations based on various conditions and it is also capable of predicting possible situations ([Bayesian Sensor)](https://www.home-assistant.io/integrations/bayesian/) but it has not been conceived to autonomously implement actions without the user having programmed them in advance.




# 4. Can you give a simpler explanation?

A home automation system designed in this way would have the advantage of being able to autonomously perform actions for a given purpose, whether it is usually achieved by the user or the consequence of other factors.

*Current Situation:*

    - There are 22°C in the house
    - The heating is off
    - The window is closed
    - The optimal temperature is 20°C
    - It's cooking at home

*Learning Model:*
    
    - When the heaters are off, the temperature in the house rises
    - When the windows are closed, the house temperature rises
    - When cooking at home temperature rises

*Decision tree:*

    - Can the radiators be turned on? [ YES ]
    - Can windows be opened? [ YES - someone is in the house to do it ]
    - Can you stop cooking ? [ NO ]

*Reasoning:*

    - Are the radiators on at this time ? [ NO ]
    - Have the radiators ever been turned on with the window open [ NO ]
    = Turn on radiators is to be discarded

*Final Solution* 

    - Open the home window or ask the user to do so.



# 5. The configuration file

The configuration file is: _apps.yaml_

- ### `hass_myhomesmart`
This is the name of the section that appDaemon wants to define the operation of the script

- #### `module`

  The name of the python file that should run

- #### `class`
  The name of the python class that must run for the script to work

- ### `config`
  the configuration section for MyHomeSmart-HASS-AppDeamon

  - ### `include_entities`
    Entities that you want to include in the MyHomeSmart system    
      -   Can enter the name of the entity as provided by HomeAssistant
          
          example: *sensor.room_temperature*

      -   Can insert the entity class to include all entities of the same class
          example: *sensor.**      
      
    The system will automatically recognize read-only entities from editable ones  

  - ### `exclude_entities`
    Entities that you want to exclude from those included in the "include_entities" section    
      -   Can enter the name of the entity as provided by HomeAssistant
          
          example: *sensor.room_temperature*

      No value indicates that no entity, included in the section "include_entities" is excluded 


# 6. How to install the script?

Follow these instructions ONLY if a stable, finished version has been released!
Look at the top of this readme !

- Install AppDeamon -> [follow here](https://appdaemon.readthedocs.io/en/latest/INSTALL.html)
  
- Open a file manager and go to folder 
  > [appDeamonFolder]/apps

- Do a gitClone of this repository:
  > git clone git@github.com:dadaloop82/MyHomeSmart-HASS-AppDeamon.git
  
  or
  
  > git clone https://github.com/dadaloop82/MyHomeSmart-HASS-AppDeamon.git

- Now you have the folder 

  > [appDeamonFolder]/apps/MyHomeSmart-HASS-AppDeamon

- Open this configuration file and modify it according to the instructions in the file

  > [appDeamonFolder]/apps/MyHomeSmart-HASS-AppDeamon/apps.yaml

- Restart AppDeamon

- Restart Home Assistant istance

- Enjoy :)
  



