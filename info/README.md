Information for the Nashville Transit GTFS Feed Project

1. Goals and Purpose

    The purpose of this project is to create a feed to real-time transit data from Nashville bus data, as well as pedestrian information. The data will store position and location of buses and record scheduling, routing, and alerts on a geospatially-enabled SQL Server. The SQL Server we will be using is Postgresql with the PostGIS extension. This is free to use and offers us the flexibility record and process information for further projects. The information will then be connected to an ArcGIS map that will be hosted and posted online for others to see.

    The extent of the analysis of these maps is still to be determined, however, the desired effect is to create useful information to analyze and possibly improve public transport and mobility in the Nashville Metropolitan Area.

2. Getting Started

    a. Current requirements
        i. ArcGIS Pro for Personal Use ($100/yr)
        ii. Postgres Connection and PostGIS Extension (free)
        iii. ArcGIS Pro Python environment (comes with ArcGIS)

    b. Installation and Set-Up (Guide on Github)
        i. Install ArcGIS Pro via myesri after creating a subscription
        ii. Install Postgresql and PostGIS
        iii. Clone ArcGIS Python environment and add to system variables
        iv. Configure dependencies for GTFS information via google
        v. Set up a Geospatial Database to store information

