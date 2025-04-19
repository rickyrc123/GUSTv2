# Ground Control Station for Uncrewed Teams and Swarms

Welcome to the homepage for GUSTv2! This project is an open source ground control system for planning missions and controlling teams and swarms of uncrewed vehicles. GUSTv2 runs on a Python FastAPI backend and uses pymavlink to connect to and command vehicles. Its front end is built in React and Electron. The program has been designed to allow for easy integration with other custom modules. 

 
  
## Core Features
 - Multiple simultaneous connections managed in real time (in progress)
 - One-Click mission execution for multi-vehicle plans (in progress)
 - Planning widget for teams (in progress)
 - Ability to design, save, edit, and upload vehicle paths multiple vehicles (in progress)
 - Real time tele-op control in case of emergencies (in progress)
 - Real time telemetry/sensor streaming and logging (in progress)
 
 ## Planned features
  - TAK integration
  - Path validator for custom vehicle types 
 <a href="page.html">page</a>

GUSTv2 aims to function as an all in one ground station for planning and controlling teams and swarms of vehicle. We want to provide a performance focused piece of software that is simple to install and use on Windows and Linux platforms. GUSTv2 is simple to modify and built on widely supported technologies. Our goal is to provide the casual user and developer alike with a robust and simple software package to control any vehicle that supports the MavLink communication protocol.

[Click Here to View the Project Pitch](presentations/GUST%20Capstone%20Pitch.pdf)

## Meet the Team
The GUST dev team consists of five seniors at the University of Alabama. We are partnered with the Laboratory for Autonomy, GNC, and Estimation Research (LAGER) on campus.

<div style="display: flex; justify-content: space-around;">
  <img src="images/nick.jpg" width="300" height="300" alt="Team Headshot">
  <img src="images/jcob_Senior_Pic.jpg" width="200" height="300" alt="Team Headshot">
  <img src="images/ricardo.jpeg" width="200" height="300" alt="Team Headshot"> 
  <img src="images/james.jpg" width="200" height="300" alt="Team Headshot">
  <img src="images/cameron.jpg" width="200" height="300" alt= "Team Headshot">
</div>

## Sprint 1 Accomplishments

In sprint 1, we established a fastAPI server to route messages between our Postgresql database and react front end. We have been making sure to use good programming standards to ensure scaliability in the future

## Sprint 2 Accomplishments

In sprint 2, we finalized our database design and have integrated the front and back end. Several screens were created in React to provide basic commmunication with the backend services. We started hardware testing.

## Key Features

## Front End Application: 

Telemetry Screen: The telemetry screen allows the user to select a single or multiple vehicles and view their positions and telemetry data such as altitude, velocity, roll, pitch, and yaw 

Path Design Screen: The path design screen will allow users to design a path for a single vehicle and combine multiple paths for multiple vehicles into a single swarm maneuver. 

Flight Screen: The flight screen will allow users to select planned manuevers and execute them. 

Connection Widget: Users will be able to easily connect to different vehicles and manage the connections. This widget will display connection strength to any of the vehicles 

Live Sensor Streaming: Users will be able to view live streamed data collected from sensors on any chose vehicle 

Emergency Protocol: In case of an emergency, the application will be able to send a safe land command to any vehicle with one button click 

Tele-Operation: Users will have the ability to fly any selected vehicle with their keyboard  

 

## Backend Services 

Persistent Database: Drone information and flight path persistence. 

Hosting: The application will run locally from a docker container that also hosts the database and other necessary services (mavlink, gazebo, etc).  

Message Routing: FastAPI will receive messages from frontend and route through mavlink to drone hardware. Also will route mavlink telemetry to the react front end. 

Auto Documentation: All endpoints will have documentation which is handled through the FastAPI app. 

Efficient API->Drone Communication: The backend aims to be as efficient as possible to be able to handle multiple drone connections. Reducing overhead is the primary driver of this. 

Mavlink Abstraction: API Endpoints will be used to abstract away some detail with sending commands to the vehicles 
 
