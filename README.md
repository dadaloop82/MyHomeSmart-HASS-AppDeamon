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

- [What does mean "Give intelligence to Home automation"?](#what-does-mean-give-intelligence-to-home-automation)
- [What is the goal of this project?](#what-is-the-goal-of-this-project)
- [Why with Home Assistant?](#why-with-home-assistant)
- [Prediction versus Logic](#prediction-versus-logic)
- [The decision tree](#the-decision-tree)
- [How to apply a logical decision tree to Home Assistant ?](#how-to-apply-a-logical-decision-tree-to-home-assistant-)
  - [Learning Block](#learning-block)
  - [Decision tree Block](#decision-tree-block)
  - [Example](#example)
  - [The benefit](#the-benefit)
  - [The potential problems](#the-potential-problems)
- [What is appDeamon?](#what-is-appdeamon)
- [How to install the script?](#how-to-install-the-script)
- ["The Reasoning" _on Hass Forum_](#the-reasoning-on-hass-forum)
- [I want to help you](#i-want-to-help-you)

#
# What does mean "Give intelligence to Home automation"?

Today we can enjoy several devices called "smart"; devices that seem to possess reasoning, logic and deduction skills in performing seemingly spontaneous actions.
In reality, this is not the case at all, each device is programmed to do actions under certain conditions, without any understanding of what it is doing and the possible consequence that such actions can do.
For example, smart speakers simply read what they find on the web, but they don't know if what they read is right or they cause the user to do the wrong thing.
A smart television is not smart, it just offers more opportunities for digital services.
And so on.

__Giving intelligence to home automation means giving a logical and comprehensive reasoning to the action that the home automation system should do to reach a certain objective.__

# What is the goal of this project?

The goal of this project is to apply to [Home Assistant (HASS)](https://github.com/home-assistant) a system of automatic creation of dynamic automations able to activate or deactivate autonomously entities to achieve the prefixed purpose, whether it is dictated by the habits of the user or it is the right thing to do to achieve a certain purpose.
Home assistant already has the ability to manually create automations based on various conditions and it is also capable of predicting possible situations ([Bayesian Sensor)](https://www.home-assistant.io/integrations/bayesian/) but it has not been conceived to autonomously implement actions without the user having programmed them in advance.

# Why with Home Assistant?

I choose  HomeAssistant over OpenHab, Domoticz or many others simply because for me it's the platform i personally prefer and in my opinion is the simplest and most comprehensive.
That's all :)

# Prediction versus Logic

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

# The decision tree

I'm not sure how to achieve this yet ( see [i want to help you](#i-want-to-help-you) ) but I think that to do this I will need one or more decision trees.
The [scikit-learn library Descision Trees](https://scikit-learn.org/stable/modules/tree.html) for Python might be useful to me for this purpose, applying the concept of Machine Learning on raw non-force numeric entities such as the states of Home Assistant entities.

The general idea could be [this below](#how-to-apply-a-logical-decision-tree-to-home-assistant-), but it could change thanks to your helping ( see [i want to help you](#i-want-to-help-you) )


# How to apply a logical decision tree to Home Assistant ?

## Learning Block
This is only a general graph concept of my idea

![Learning Block](https://github.com/dadaloop82/MyHomeSmart-HASS-AppDeamon/raw/main/images/MyHomeSmart-concept.drawio.learningblock.png)

## Decision tree Block
This is only a general graph concept of my idea

## Example

## The benefit

## The potential problems

# What is appDeamon?

# How to install the script?

# "The Reasoning" _on Hass Forum_
https://community.home-assistant.io/t/reasoning-artificial-intelligence-applied-to-home-assistant/408972

#  I want to help you