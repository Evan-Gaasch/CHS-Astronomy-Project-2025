#V0 but with heatmap graphing/porkchop plot
"""
Filename: mission-simulation-v1.py
Version: 1.0
Description: Astronomy Club Project (Mission Simulation using Poliastro)
"""
#Assumptions: Assume we start with 1st stage already burnt, in low earth orbit (this is true for most large modern rockets, though small rockets have not reached orbit when they burn their first stage)
#Assume round initial orbit (e=0) to simplify calculations

#import astropy sub-packages
import poliastro
from astropy import units
from astropy.time import Time, TimeDelta
from poliastro.bodies import Body, Earth, Mars, Jupiter, Mercury, Saturn, Venus, Uranus, Neptune,Sun #add more here if you want different objects
from poliastro.twobody import Orbit
from poliastro.iod.izzo import lambert
from dataclasses import dataclass, field
import poliastro.maneuver as maneuver
import matplotlib.pyplot as plt #graphing libraries
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

    targetBody: Body = Neptune #planet or other supported poliastro object
    targetOrbitAltitude: int = 300 *units.km
    targetOrbitInclination: float = 0.0 * units.deg
    
    launchWindowStartDate: Time = field(default_factory=lambda: Time("2030-01-01", scale="tdb")) #useful for finding trajectories with minimum delta v
    launchWindowEndDate: Time = field(default_factory=lambda: Time("2031-01-01", scale="tdb"))
    tof_max = 10000
    tof_min = 1000
    #add other parameters like rocket type here


def approximateTOF():
    #fill in this function later, now just guess some number of days

    # function here will use lambert solver to find minimum, upper bound of time and search through that for a solutions
    
    return (400* units.day) #rough guess


def calcDepartureBurn(v_depart, departure_trajectory, parkingAltitude, departBody):
    
    v_inf_depart = np.linalg.norm((v_depart - departure_trajectory.v).to(units.km / units.s).value)
    
    # parking orbit radius = body radius + altitude
    r_park = (departBody.R + parkingAltitude).to(units.km).value
    mu = departBody.k.to(units.km**3 / units.s**2).value
    
    # velocity in parking orbit
    v_circ = np.sqrt(mu / r_park)
    
    # velocity needed at periapsis of departure hyperbola
    v_hyp = np.sqrt(v_inf_depart**2 + 2 * mu / r_park)
    
    return v_hyp - v_circ  # delta-V for the burn

def calcArrivalBurn(v_arrive, arrival_trajectory, parkingAltitude, arriveBody):
    v_inf_arrive = np.linalg.norm((arrival_trajectory.v - v_arrive).to(units.km / units.s).value)
    
    r_park = (arriveBody.R + parkingAltitude).to(units.km).value
    mu = arriveBody.k.to(units.km**3 / units.s**2).value
    
    v_circ = np.sqrt(mu / r_park)
    v_hyp = np.sqrt(v_inf_arrive**2 + 2 * mu / r_park)
    
    return v_hyp - v_circ
            

def lambertSolver(launchDate,timeOfFlight): #add more parameters here when time of flight is calculated automatically
    params = InitialParameters()
    #timeOfFlight = approximateTOF() #seconds
    arrivalDate = launchDate + TimeDelta(timeOfFlight)
    #print("Date",arrivalDate)

    #find initial positions of start and end points of transfer (interplanetary section)
    departure_trajectory = Orbit.from_body_ephem(params.startingBody, epoch=launchDate)
    arrival_trajectory = Orbit.from_body_ephem(params.targetBody, epoch=arrivalDate)

    

    (v_depart, v_arrive), = lambert(Sun.k, departure_trajectory.r, arrival_trajectory.r, tof = timeOfFlight.to(units.s))

    #calculate burn required to exit initial orbit, enter final orbit

    departure_burn = calcDepartureBurn(v_depart, departure_trajectory, params.initialOrbitAltitude, params.startingBody)
    arrival_burn = calcArrivalBurn(v_arrive, arrival_trajectory, params.targetOrbitAltitude, params.targetBody)

    cost = departure_burn+arrival_burn #all delta v provided at start and end, you "coast" during lambert transfer
    #print(cost)
    return cost


def main():
    params = InitialParameters()
    print("main starting")
    data = {
        "startTime":[],
        "timeOfFlight":[],
        "deltaVcost":[],
        }
    print(type(params.launchWindowEndDate))
    launchDate = params.launchWindowStartDate
    while launchDate < params.launchWindowEndDate:
        for tof in range (params.tof_min, params.tof_max,10):
            mission_tof = (tof*units.day).to(units.s)
            cost = lambertSolver(launchDate,mission_tof)
            data["startTime"].append(launchDate.to_datetime())
            data["timeOfFlight"].append(tof)
            data["deltaVcost"].append(cost)

        #increment time by timestep
        launchDate = launchDate + TimeDelta(25* units.day)

    print(data)
    df = pd.DataFrame(data)
    #plot final results
    #df.plot(x="startTime", y="deltaVcost",   kind = "scatter")
    #plt.show()

    #plot heatmap
    tof_values = np.array((df["timeOfFlight"].unique()))
    date_values = np.array((df["startTime"].unique()))
    dv_grid = np.array(df["deltaVcost"]).reshape(len(date_values), len(tof_values))

    plt.figure()
    plt.contourf(tof_values, date_values, dv_grid, levels=50, cmap="viridis")
    plt.colorbar(label="Delta-V (km/s)")
    plt.xlabel("Time of Flight (days)")
    plt.ylabel("Launch Date")
    plt.title("Time of flight and launch date vs delta v")
    plt.show()
    return df

main()
  
    

    
  
