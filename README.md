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

[ Table of Content ]

- [1. Project Progress](#1-project-progress)
- [2. What does mean "Give intelligence to Home automation"?](#2-what-does-mean-give-intelligence-to-home-automation)
- [3. What is the goal of this project?](#3-what-is-the-goal-of-this-project)
- [4. Why with Home Assistant?](#4-why-with-home-assistant)
- [5. Prediction versus Logic](#5-prediction-versus-logic)
- [6. The decision tree](#6-the-decision-tree)
- [7. How to apply this to Home Assistant ?](#7-how-to-apply-this-to-home-assistant-)
  - [7.1. Hypothetical operation diagram](#71-hypothetical-operation-diagram)
  - [7.2. Can you give a simpler explanation?](#72-can-you-give-a-simpler-explanation)
  - [7.3. Cool! But what are the difficulties?](#73-cool-but-what-are-the-difficulties)
- [8. What is appDeamon?](#8-what-is-appdeamon)
- [9. How to install the script?](#9-how-to-install-the-script)
- [10. "The Reasoning" _on Hass Forum_](#10-the-reasoning-on-hass-forum)
- [11. Cool! How can I help you?](#11-cool-how-can-i-help-you)
#

# 1. Project Progress

| ![Overall](https://progress-bar.dev/0/?scale=100&title=Overall&width=420&suffix=%) |
| :--------------------------------------------------------------------------------- |

| ![Idea description](https://progress-bar.dev/70/?title=idea%20description&width=140) | ![Data collection](https://progress-bar.dev/0/?title=data%20collection&width=140) |
| :----------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------- |
| ![Learning stage](https://progress-bar.dev/0/?title=learning%20stage&width=150)      | ![Reasoning stage](https://progress-bar.dev/0/?title=reasoning%20stage&width=140) |
| ![Solution provide](https://progress-bar.dev/0/?title=solution%20provide&width=140)  | ![Testing](https://progress-bar.dev/0/?title=testing&width=190)                   |              |

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

# 4. Why with Home Assistant?

I choose  HomeAssistant over OpenHab, Domoticz or many others simply because for me it's the platform i personally prefer and in my opinion is the simplest and most comprehensive.
That's all :)

# 5. Prediction versus Logic

In the world of Home Assistant, prediction is understood as the triggering of a certain event based on the possibilities that this event has already occurred in the same situation.

_Example_:

    When the temperature drops below 20°C, except at night, I always turn on the radiators.

The predictive automatism will then check when the temperature is below 20°C and if it is night or day, if so it will turn on the radiators.

- _But what if there is a window open in the house?_
- _Or if no one is home?_
- _Or if you're cooking dinner soon and therefore the temperature would rise without turning on the heaters?_

The system would not consider these factors and would simply turn on the heating, forcing the user to manually intervene so as not to create discomfort.

Applying *Logic and Reasoning* to the actions to be taken means giving Home Assistant a learning system of all the possible situations that can generate (or have generated) a certain result and decide for themselves which action is the most logical to do.
Surely it will need a lot of initial learning, but when it knows, for example, that the open window lowers the temperature, it will avoid turning on the heating because it would not obtain the desired result.

# 6. The decision tree

I'm not sure how to achieve this yet ( [maybe you can help me?](#11-cool-how-can-i-help-you) ) but I think that to do this I will need one or more decision trees.
The [scikit-learn library Descision Trees](https://scikit-learn.org/stable/modules/tree.html) for Python might be useful to me for this purpose, applying the concept of Machine Learning on raw non-force numeric entities such as the states of Home Assistant entities.

The general idea could be [this below](#how-to-apply-a-logical-decision-tree-to-home-assistant-), but it could change thanks to your helping.


# 7. How to apply this to Home Assistant ?

## 7.1. Hypothetical operation diagram
This is only a general graph concept of my idea: if you have a better or another idea please see ( [maybe you can help me?](#11-cool-how-can-i-help-you) ) sections

![Hypothetical operation diagram](https://github.com/dadaloop82/MyHomeSmart-HASS-AppDeamon/raw/main/images/MyHomeSmart-concept-learningBlock.drawio.png)

## 7.2. Can you give a simpler explanation?

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


## 7.3. Cool! But what are the difficulties?

The main difficulty is to transform an idea into a programmable solution: I've already tried many times to do something like this, but I've always had to stop in front of technical and/or implementation limits that are difficult or impossible to overcome.
Since I have (or we have, thanks to you!) clear ideas we can certainly proceed with more confidence even having to change the initial idea, if necessary.
( [maybe you can help me?](#11-cool-how-can-i-help-you) )


# 8. What is appDeamon?

(from https://appdaemon.readthedocs.io/en/latest/HASS_TUTORIAL.html)

AppDaemon is a subsystem to complement Home Assistant’s Automation and Scripting components. AppDaemon, is a Python daemon that consumes events from Home Assistant and feeds them to snippets of Python code called Apps. An App is a Python class that is instantiated possibly multiple times from AppDaemon and registers callbacks for various system events. It is also able to inspect and set state and call services. The API provides a rich environment suited to home automation tasks that can also leverage all the power of Python.

# 9. How to install the script?

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
  

# 10. "The Reasoning" _on Hass Forum_
  >  https://community.home-assistant.io/t/reasoning-artificial-intelligence-applied-to-home-assistant/408972

#  11. Cool! How can I help you?