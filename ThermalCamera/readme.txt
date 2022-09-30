Hello! This is a project of a fire-detecting drone.

In order to achieve this, we used a thermal camera and a GPS.

How it works:
The thermal camera will attempt to detect areas with large amounts of heat (>200 C)
Then the GPS will return the location of the drone.

ssh: pt0-flightpi

To ensure proper functionality, make sure to put these lines on the config.txt found in the root file
of the Raspberry Pi:
dtoverlay=uart4
dtoverlay=uart5