"""
Filename: mission-simulation-v1.py
Version: 1.0
Description: Astronomy Club Project (Mission Simulation using Poliastro)
"""
#Assumptions: Assume we start with 1st stage already burnt, in low earth orbit (this is true for most large modern rockets, though small rockets have not reached orbit when they burn their first stage)
#Assume round initial orbit (e=0) to simplify calculations

#import astropy sub-packages
from astropy import units
from astropy.time import Time, TimeDelta
from poliastro.bodies import Body, Earth, Mars, Jupiter, Mercury, Saturn, Venus, Uranus, Neptune #add more here if you want different objects
from poliastro.twobody import Orbit
from dataclasses import dataclass, field
import poliastro.maneuver as maneuver
import matplotlib #graphing libraries
import numpy as np
import pandas as pd
print("Initializing")
print(poliastro.__version__)

#Set Parameters Here:
@dataclass
class InitialParameters:
    payload: int = 500 #kilograms
    
    startingBody: Body = Earth
    launchSiteLatitude: int = 28.5* units.deg #Kennedy Space Center is at this inclination, latitude = inclination is a good assumption as it is hard to change inclination once in LE
    initialOrbitAltitude: float = 300* units.km#km, above target planet's surface

    targetBody: Body = Mars #planet or other supported poliastro object
    targetOrbitAltitude: int = 300 *units.km
    targetOrbitInclination: float = 0.0 * units.deg
    
    launchWindowStartDate: Time = field(default_factory=lambda: Time("2030-01-01", scale="tdb")) #useful for finding trajectories with minimum delta v
    launchWindowEndDate: Time = field(default_factory=lambda: Time("2031-01-01", scale="tdb"))
    #add other parameters like rocket type here

    
#Define initial orbit:
def createInitialOrbit(launchDate):
    params = InitialParameters()
    return Orbit.circular(
        attractor=params.startingBody,
        inc=params.launchSiteLatitude,
        alt=params.initialOrbitAltitude,
        epoch=launchDate
    )

def createArrivalOrbit(arrivalDate):
    params = InitialParameters()
    return Orbit.circular(
        attractor=params.targetBody,
        inc=params.targetOrbitInclination,
        alt=params.targetOrbitAltitude,
        epoch=arrivalDate
    )

def approximateTOF():
    #fill in this function later, now just guess some number of days

    # function here will use lambert solver to find minimum, upper bound of time and search through that for a solutions
    
    return (400) 

def lambertSolver(launchDate): #add more parameters here when time of flight is calculated automatically

    timeOfFlight = approximateTOF()
    arrivalDate = launchDate + TimeDelta(timeOfFlight* units.day)
    print("Date",arrivalDate)

    initialOrbit = createInitialOrbit(launchDate)
    arrivalOrbit = createArrivalOrbit(arrivalDate)

    lambertTransfer = maneuver.Maneuver.lambert(initialOrbit,arrivalOrbit,method=lambert_izzo)

    cost = lamberTransfer.get_total_cost()
    print(cost)
    return cost


def main():
    params = InitialParameters()
    print("main starting")
    data = {
        "startTime":[],
        "deltaVcost":[],
        }
    print(type(params.launchWindowEndDate))
    launchDate = params.launchWindowStartDate
    while launchDate < params.launchWindowEndDate:
        cost = lambertSolver(launchDate)
        data["startTime"].append(launchDate)
        data["deltaVcost"].append(cost)

        #increment time by timestep
        launchDate = launchDate + TimeDelta(25* units.day)

    print(data)
    df = pandas.DataFrame(data)
    #plot final results
    df.plot()
    return df

main()    
