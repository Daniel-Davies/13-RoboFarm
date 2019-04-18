---
layout: default
title:  Proposal
---

## Minecraft Farming AI

Farming in minecraft can be quite a time consuming process, that involves quite a number of variables.
For this reason, we are hoping to make an agent that can automate it for the user.





## Summary of the Project

There are quite a number of variables involved in farming in minecraft. These include:

- Terrain: which block you place seeds on directly influences crop yield
- Proximity to water: the closer to a river/water, the faster crops grow
- Light: even if artificial, more light generally means a higher crop yield
- Material Additions: Materials like Bone Meal can help make crop yield faster

We have prepared a number of goals to reach:

- MVP: We want the AI to realise that planting in Rock is bad and in Grass is good
- Then hopefully we can allow our AI to start optimising by realising ploughed grass is even better
- Finally we will try and allow the AI to reach optimal farming methods, e.g., using Bone Meal to speed things up

The more points we can cross off this list, the better we can say an agent is at farming, and the more trust a user would have
in letting the AI manage the seeds a user has to reap rewards over a number of minecraft days.

Input to our AI: The malmo API will let us generate worlds with a number of terrains, and also have access to these terrains as a
JSON array, which show which blocks we have at a given location. We will also take in the number of seeds a user has to plant.

Output: the agent will produce a set of actions to move around the world, searching for what it believes to be optimal blocks to plant in, and product 
a plant action once it is satisifed that it has found one.

Applications: Essentially, the project allows a player to automate farming, which can take a long time in minecraft.    

Now that we have a goal and some variables, we can describe some stages:

- Stage one: how do we get our data/ input from the world?
    Malmo will provide us with the methods needed to read the world. This will be especially important to start
    when we teach our AI about the terrain that it should plant on.
    We will most likely initialise a world conatining a number of terrains, e.g. Rock, Grass, and Ploughed Grass,
    and allow the Agent, with it's reward function, to identify optimal spaces to plant in.
- The reward function:
    This will most likely be the amount of wheat collected. To ensure fairness, we will cut off the mission after a 
    fixed period, e.g. 2 minecraft days of growing.
- What to expect:
    - Ploughed grass will have the most wheat. 
    - Grass will have some. 
    - Rock will have none.
- Influencing the world/ what will our output be?
    Our output will essentally be a list of actions from our reinforcement learning algorithm.
    The actions will essentially be:
    - Move to a location
    - Plant at a given location
    - Add a material on top of crops (Bone Meal for example) as an eventual target
    A list of such actions will then be given to the Malmo API to execute.
- Progress Tracking
    Initially we need to produce a "random agent" -> an agent that, completely randomly, plants a seed on a random block.
    We will then measure the success of this agent using the cutoff metric described above. 
    Once we have this data, we will continue to train our agent and compare the agent to this random success rate.
