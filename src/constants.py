class UniversalConstants:

    # Gravitational constant (km^3/kg/s^2):
    G = 6.6743e-20

    # Astronomical unit (km)
    AU = 149597870.7

    #Seconds per day
    SECONDS_PER_DAY = 86400

class Sun:

    #Gravitational parameter MU☉ (km^3/s^2)
    MU = 1.327e11

     #Solar radius (km)
    RADIUS = 695700

class Planets:

    #Gravitational Parameters (km^3/s^2)
    MU_MERCURY = 2.2032e4
    MU_VENUS = 3.24859e5
    MU_EARTH = 3.986004418e5
    MU_MARS = 4.282837e4
    MU_JUPITER = 1.26686534e8
    MU_SATURN = 3.7931187e7
    MU_URANUS = 5.793939e6
    MU_NEPTUNE = 6.836529e6

    #Equatorial radii (km)
    R_MERCURY = 2.4397e3
    R_VENUS = 6.0518e3
    R_EARTH = 6.3781e3
    R_MARS = 3.3962e3
    R_JUPITER = 71492
    R_SATURN = 60268
    R_URANUS = 25559
    R_NEPTUNE = 24764

    #Minimum flyby distance (km)
    #Add Equatorial radii to find total flyby radius
    MIN_FLYBY_MERCURY = 200
    MIN_FLYBY_VENUS = 300
    MIN_FLYBY_EARTH = 300
    MIN_FLYBY_MARS = 150
    MIN_FLYBY_JUPITER = 2000
    MIN_FLYBY_SATURN = 2000
    MIN_FLYBY_URANUS = 1000
    MIN_FLYBY_NEPTUNE = 1000
