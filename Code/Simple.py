from __future__ import print_function
# ------------------------------------------------------------------------------------------------
# Copyright (c) 2016 Microsoft Corporation
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------------

# Tutorial sample #2: Run simple mission using raw XML

from builtins import range
from math import hypot, sqrt
import MalmoPython
import os
import sys
import time
import json
import random
import collections

if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools

    print = functools.partial(print, flush=True)

# More interesting generator string: "3;7,44*49,73,35:1,159:4,95:13,35:13,159:11,95:10,159:14,159:6,35:6,95:6;12;"

#num_seeds = 10
def generateMissionXML(inputWorld):
    generatedMissionXML = '''<?xml version="1.0" encoding="UTF-8" ?>
    <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <About>
            <Summary></Summary>
        </About>

        <ModSettings>
            <MsPerTick>1</MsPerTick>
        </ModSettings>

        <ServerSection>
            <ServerInitialConditions>
                <Time>
                    <StartTime>6000</StartTime>
                    <AllowPassageOfTime>false</AllowPassageOfTime>
                </Time>
                <Weather>clear</Weather>
                <AllowSpawning>false</AllowSpawning>
            </ServerInitialConditions>
            <ServerHandlers>
                <FlatWorldGenerator generatorString="3;7,220*1,5*3,2;8;,biome_1" />
                <DrawingDecorator>
                    '''+ inputWorld + '''
                </DrawingDecorator>
                <ServerQuitWhenAnyAgentFinishes />
            </ServerHandlers>
        </ServerSection>

        <AgentSection mode="Survival">
            <Name>Odie</Name>
            <AgentStart>
                <Placement x="0.5" y="226.0" z="0.5" yaw="90"/>
                <Inventory>
                    <InventoryItem slot="0" type="wheat_seeds" quantity="''' + str(10) + '''"/>
                </Inventory>
            </AgentStart>
            <AgentHandlers>
                <ContinuousMovementCommands turnSpeedDegs="480"/>
                <AbsoluteMovementCommands/>
                <SimpleCraftCommands/>
                <MissionQuitCommands/>
                <InventoryCommands/>
                <ObservationFromNearbyEntities>
                    <Range name="entities" xrange="40" yrange="40" zrange="40"/>
                </ObservationFromNearbyEntities>
                <ObservationFromFullInventory/>
                <ObservationFromGrid>
                    <Grid name="crops20x20">
                    <min x="-10" y="0" z="-10"/>
                    <max x="10" y="0" z="10"/>
                    </Grid>
                    <Grid name="crops30x30">
                    <min x="-15" y="0" z="-15"/>
                    <max x="15" y="0" z="15"/>
                    </Grid>
                    <Grid name="crops40x40">
                    <min x="-20" y="0" z="-20"/>
                    <max x="20" y="0" z="20"/>
                    </Grid>
                    <Grid name="crops50x50">
                    <min x="-25" y="0" z="-25"/>
                    <max x="25" y="0" z="25"/>
                    </Grid>
                </ObservationFromGrid>
                <AgentQuitFromCollectingItem>
                    <Item type="rabbit_stew" description="Supper's Up!!"/>
                </AgentQuitFromCollectingItem>
            </AgentHandlers>
        </AgentSection>

    </Mission>'''
    return generatedMissionXML

missionXML_split_water = generateMissionXML(
''' 
                    <DrawCuboid x1="-50" y1="226" z1="-50" x2="50" y2="228" z2="50" type="air" />
                    <DrawCuboid x1="-50" y1="226" z1="-50" x2="50" y2="226" z2="50" type="stone" />                    
                    <DrawCuboid x1="-25" y1="226" z1="-25" x2="25" y2="226" z2="25" type="farmland" />
                    <DrawCuboid x1="-25" y1="226" z1="20" x2="-20" y2="226" z2="25" type="water" />
                    <DrawCuboid x1="20" y1="226" z1="-20" x2="25" y2="226" z2="-25" type="water" />
                    ''')

missionXML_hell = generateMissionXML(''' 
                    <DrawCuboid x1="-50" y1="226" z1="-50" x2="50" y2="228" z2="50" type="air" />
                    <DrawCuboid x1="-50" y1="226" z1="-50" x2="50" y2="226" z2="50" type="stone" />                    
                    <DrawCuboid x1="-10" y1="226" z1="-10" x2="10" y2="226" z2="10" type="farmland" />
                    <DrawCuboid x1="0" y1="226" z1="0" x2="0" y2="226" z2="0" type="water" />
                    <DrawCuboid x1="-10" y1="226" z1="-10" x2="-10" y2="226" z2="-10" type="grass" />
                    <DrawCuboid x1="10" y1="226" z1="10" x2="10" y2="226" z2="10" type="grass" />
                    <DrawCuboid x1="9" y1="226" z1="10" x2="9" y2="226" z2="10" type="grass" />
                    ''')

#                 <DrawCuboid x1="-10" y1="226" z1="-10" x2="-10" y2="226" z2="-10" type="grass" />
#                 <DrawCuboid x1="10" y1="226" z1="10" x2="10" y2="226" z2="10" type="grass" />
#                 <DrawCuboid x1="9" y1="226" z1="10" x2="9" y2="226" z2="10" type="grass" />

missionXML_surrounding_water = generateMissionXML(''' 
                    <DrawCuboid x1="-50" y1="226" z1="-50" x2="50" y2="228" z2="50" type="air" />
                    <DrawCuboid x1="-50" y1="226" z1="-50" x2="50" y2="226" z2="50" type="water" />                    
                    <DrawCuboid x1="-10" y1="226" z1="-10" x2="10" y2="226" z2="10" type="farmland" />
                    <DrawCuboid x1="-2" y1="226" z1="-2" x2="2" y2="226" z2="2" type="stone" />
                    ''')

#point will be to restrict generation of seeds to one corner only
missionXML_corner_water = generateMissionXML(''' 
                    <DrawCuboid x1="-50" y1="226" z1="-50" x2="50" y2="228" z2="50" type="air" />
                    <DrawCuboid x1="-50" y1="226" z1="-50" x2="50" y2="226" z2="50" type="stone" />                    
                    <DrawCuboid x1="-20" y1="226" z1="-20" x2="20" y2="226" z2="20" type="farmland" />
                    <DrawCuboid x1="15" y1="226" z1="-15" x2="20" y2="226" z2="-20" type="water" />
                    ''')

NUM_ROWS = 31
NUM_COLS = 31

def getAverageEuclidean(pointslist):
    total = 0
    for pt in pointslist:
        total = total + averageEuclideanDist(pt, pointslist)
    
    return total / len(pointslist)


def averageEuclideanDist(point, pointlist):
    total = 0
    for pt in pointlist:
        xa, ya = point
        xb, yb = pt
        dist = sqrt((xa-xb)**2 + (ya-yb)**2)
        total = total + dist
    return total / (len(pointlist) - 1)


def teleport(agent_host, teleport_x, teleport_z):
    """Directly teleport to a specific position."""
    tp_command = "tp " + str(teleport_x) + " 226 " + str(teleport_z)
    agent_host.sendCommand(tp_command)
    good_frame = False


def plant_random(mapsize, num_seeds):
    planting = []
    for i in range(num_seeds):
        x = random.randint(-mapsize, mapsize)
        y = random.randint(-mapsize, mapsize)
        planting.append((x, y))

    return planting


def initialise_planting_coords(mapsize, num_seeds, water):
    seed_locations = []
    while (True):
        x = random.randint(-mapsize, mapsize)
        y = random.randint(-mapsize, mapsize)
        if ((x, y) not in seed_locations and (x,y) not in water):
            seed_locations.append((x, y))
        if (len(seed_locations) == num_seeds):
            break
    return seed_locations


def breed(parent1, parent2):
    parents = [parent1[0], parent2[0]]
    x = random.randint(0, 1)
    y = random.randint(0, 1)

    return ((parents[x])[0], (parents[y])[1])

breakVals = []


def cross_over(best, water, num_seeds):
    # return a list of children
    best_tuples = []
    for i in best:
        best_tuples.append(i[0])
    newchilren = []
    genLimit = len(best)
    if (num_seeds & 1):
        genLimit = genLimit + 1
    for i in range(genLimit):
        parent1 = best[random.randint(0, len(best) - 1)]
        parent2 = best[random.randint(0, len(best) - 1)]
        new_coord = breed(parent1, parent2)
        while (True):
            if (new_coord in best_tuples or new_coord in newchilren or new_coord in water):
                x, z = new_coord
                x = x + 1
                z = z - 1
                new_coord = (x, z)
            else:

                newchilren.append(new_coord)
                break
    return newchilren


def mutate(coordinate, round_num, mapsize):
    if (round_num < (10-5)):
        x, y = coordinate
        offsetX = random.randint(-mapsize+round_num, mapsize-round_num)
        offsetY = random.randint(-mapsize+round_num, mapsize-round_num)
        x = x + offsetX
        y = y + offsetY
        return (x, y)
    else:
        return coordinate


def select_elite_seeds(scores_tuples):
    # return top 50%- they made it to the next round
    top50 = len(scores_tuples) / 2
    return scores_tuples[0:int(top50)]


def select_weaker_seeds(scores_tuples):
    # return top 50%- they made it to the next round
    top50 = len(scores_tuples) / 2
    return scores_tuples[int(top50):]


def score_seeds(seed_locations, dirt, rock, water):
    scores = dict()

    '''
        Reward hydrated crops
    '''
    for seed_tup in seed_locations:
        if seed_tup in rock or seed_tup in water:
            # Invalid seed placement -> 0.0 score
            scores[seed_tup] = 0.0
        else:
            # Calculate distance from each water coordinate and score based on minimum
            water_distances = []
            for water_tup in water:
                water_distances.append(hypot(water_tup[0] - seed_tup[0], water_tup[1] - seed_tup[1]))
            water_dist = min(water_distances) if len(water) > 0 else 0.0

            max_distance = sqrt(200)  # sqrt(10^2 + 10^2), will vary based on map size
            raw_score = max_distance - water_dist
            if water_dist <= 4.0:
                # Hydrated farmland
                scores[seed_tup] = raw_score
            else:
                # Dry farmland -> apply flat penalty.  Minimum score 1.0
                scores[seed_tup] = 1.0 if (raw_score - 2.0) < 1.0 else raw_score - 2.0


    '''
         Reward crops planted consecutively in columns
    '''
    columns = collections.defaultdict(list)
    for seed_tup in seed_locations:
        columns[seed_tup[1]].append(seed_tup)

    for col_list in columns.values():
        in_order = sorted(col_list, key=(lambda x : x[0]))

        max_consec = 1
        current_consec = 1
        seeds_set = set()
        max_seed_set = set()
        for i in range(-len(in_order), len(in_order)-1):
            if (in_order[i][0] + 1) == in_order[i+1][0]:
                current_consec += 1
                if current_consec > max_consec:
                    max_consec = current_consec
                    max_seed_set = seeds_set
                seeds_set.add(in_order[i+1])
            else:
                current_consec = 1
                seeds_set = set()
                seeds_set.add(in_order[i])

        # Add extra score to any consecutive sequence in a column size 3 or more
        if max_consec >= 3:
            for seed_tup in max_seed_set:
                scores[seed_tup] += 0.5

    #print(seed_locations)
    #print(scores)
    return scores.items()


##########################
####changes based on the map
##############################
def calculateOptimalRange():
    optimal = set()
    for i in range(-4, 5):
        for j in range(-4, 5):
            optimal.add((i, j))
    return optimal

def inRange(optimal, point):
    return (point in optimal)

def calculateVariance(scoresHistory):
    if(len(scoresHistory) < 10):
        return 10
    previous10 = scoresHistory[len(scoresHistory)-10:]   
    listAvg = sum(previous10) / len(previous10)
    differences = list(map(lambda x: abs(x - listAvg), previous10))
    unreasonableVariations = len([x for x in differences if (x > 5)])
    return unreasonableVariations

def shouldLoopBreak(varianceList):
    if(len(varianceList) < 10):
        return False
    previous10 = varianceList[len(varianceList)-10:]

    return (len([x for x in previous10 if (x < 5)]) > 5)


def scoreInRange(coords):
    return sum(map(lambda x: inRange(calculateOptimalRange(), x), coords))

def getBestPlantingCoords(dirt, rock, water, num_seeds):
    planting_coords = initialise_planting_coords(10, num_seeds, water)
    #print()
    #print("Round 1")
    #print(planting_coords)
    # for now lets do 10 rounds
    initialRounds = 30
    scoresHistory = []
    maxScore = 0
    maxAtRound = 0
    maxConfiguration = planting_coords

    unreasonableVariations = []
    for loopVal in range(initialRounds):
        scores = score_seeds(planting_coords, dirt, rock, water)  # as a
        #print("Scores_" + str(loopVal) + " = " + str([i[1] for i in scores]))
        planting_coords = []

        scores = sorted(scores, key=lambda x: x[1])[::-1]

        scoresHistory.append(sum([x[1] for x in scores]))

        if (sum([x[1] for x in scores]) > maxScore):
            maxScore = sum([x[1] for x in scores])
            maxAtRound = loopVal
            maxConfiguration = planting_coords

        best = select_elite_seeds(scores)

        for i in best:
            planting_coords.append(i[0])

        children = cross_over(best, water, num_seeds)

        for i in children:
            planting_coords.append(i)

        if (loopVal < 5):
            mutation = None
            mutated = None
            while(True):
                mutation = random.randint(0, len(planting_coords) - 1)
                #print("Pre-mutation: " + str(planting_coords[mutation]))
                mutated = mutate(planting_coords[mutation], loopVal, 10)
                #print("Post-mutation: " + str(mutated))
                if not(mutated in planting_coords) and not(mutated in water):
                    break
            planting_coords[mutation] = mutated

        unreasonableVariations.append(calculateVariance(scoresHistory));
        if(shouldLoopBreak(unreasonableVariations)):
            #print("Broken on " + str(loopVal))
            breakVals.append(loopVal)
            break

    return maxConfiguration


agent_host = MalmoPython.AgentHost()

try:
    agent_host.parse(sys.argv)
except RuntimeError as e:
    print('ERROR:', e)
    print(agent_host.getUsage())
    exit(1)
if agent_host.receivedArgument("help"):
    print(agent_host.getUsage())
    exit(0)

#teleport him out of water square
teleport(agent_host,2,2)

my_mission = MalmoPython.MissionSpec(missionXML_surrounding_water, True)
my_mission_record = MalmoPython.MissionRecordSpec()

# Attempt to start a mission:
max_retries = 3
for retry in range(max_retries):
    try:
        agent_host.startMission(my_mission, my_mission_record)
        break
    except RuntimeError as e:
        if retry == max_retries - 1:
            print("Error starting mission:", e)
            exit(1)
        else:
            time.sleep(2)

# Loop until mission starts:
print("Waiting for the mission to start ", end=' ')
world_state = agent_host.getWorldState()
while not world_state.has_mission_begun:
    print(".", end="")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print("Error:", error.text)

time.sleep(1)
#agent_host.sendCommand("pitch 0.5")

print()
obs = agent_host.getWorldState().observations
for item in obs:
    js_dict = json.loads(item.text)

print()
print()

dirt = set()
rock = set()
water = set()

print(js_dict['crops30x30'])

raw_index = 0
for block in js_dict['crops30x30']:
    row = int(raw_index / NUM_COLS)-10
    col = (raw_index % NUM_COLS)-10
    raw_index += 1

    if block == 'dirt' or block == 'farmland':
        dirt.add((row, col))
    elif block == 'stone':
        rock.add((row, col))
    elif block == 'water':
        water.add((row, col))

print("FOUND THIS MANY WATER BLOCKS:   ", len(water))


time.sleep(2)
teleport(agent_host, 4, 4)

print("Mission running ", end=' ')


teleport(agent_host,2,2)
'''
for i in range(-10, 11):
    for j in range(-10, 11):
        dirt.add((i, j))

water.add((0, 0))

for i in water:
    dirt.remove(i)

dirt = list(dirt)
rock = list(rock)
water = list(water)
'''
agent_host.sendCommand("pitch 0.5")
time.sleep(5)

planting_coords = []
scoresVal = []

intemediary = []

#for vary_seeds in range(1000):
    #planting_coords = getBestPlantingCoords(dirt, rock, water, 10)
    #intemediary.append(getAverageEuclidean(planting_coords))
    #print(str(scoreInRange(planting_coords)) + " seeds were successfully planted in the hydrated zone")

#print()
#print(planting_coords)

planting_coords = getBestPlantingCoords(dirt, rock, water, 10)


scoresVal.append(scoreInRange(planting_coords))
print(str(scoreInRange(planting_coords)) + " seeds were successfully planted in the hydrated zone")

#print(scoresVal)

#print("Average is " + str(sum(scoresVal)/len(scoresVal)))

agent_host.sendCommand("pitch 1")
time.sleep(5)
planted_indices = []
for i in range(0, len(planting_coords)):
    x, z = planting_coords[i]
    print("planting: ", x, " ", z)
    if ((x, z) in rock):
        print("Hit rock")
    teleport(agent_host, x, z)
    time.sleep(2);
    agent_host.sendCommand("use 1")
    planted_indices.append(i)

time.sleep(5)
for i in planted_indices:
    x, z = planting_coords[i]
    teleport(agent_host, x, z)
    time.sleep(2);
    print("removing: ", x, " ", z)
    agent_host.sendCommand("attack 1")
    time.sleep(0.1)
    agent_host.sendCommand("attack 0")

'''
# Loop until mission ends:
while world_state.is_mission_running:
    print(".", end="")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print("Error:",error.text)
'''

print()
print("Mission ended")
# Mission has ended.
agent_host.sendCommand("attack 0")
# pitch up etc
