import MapComponent from "./MapComponent.jsx";
import DroneList from "./DroneSelection.jsx";
import AltimeterGauge from "./AltimeterGauge.jsx";
import ManeuverList from "./HomeManeuverSelect.jsx";
import ArmButton from "./ArmButton.jsx"
import { useState, useEffect } from "react";

function HomeScreen() {
    const [selectedDrone, setSelectedDrone] = useState(null);
    const [selectedManeuver, setSelectedManeuver] = useState(null);
    const [maneuverDrones, setManeuverDrones] = useState([]);
    const [drones, setDrones] = useState([]);
    const [maneuvers, setManeuvers] = useState([]);

    
  
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch("http://localhost:8000/drones");
                const data = await response.json();
                setDrones(data.Drones || []);

                const maneuverResponse = await fetch("http://localhost:8000/maneuvers");
                const maneuver = await maneuverResponse.json();
                setManeuvers(maneuver.maneuvers || []);
                

            } catch (error) {
                console.error("Error fetching data:", error);
            }
        };

        fetchData();
        const interval = setInterval(fetchData, 1000);
        return () => clearInterval(interval);
    }, []);

    useEffect(() => {
        const fetchManeuverDrones = async () => {
            if (selectedManeuver) {
                try {
                    const maneuverDronesResponse = await fetch(`http://localhost:8000/programs/manuevers/get_drones_in_maneuver?maneuver_name=${selectedManeuver}`, {
                        method: "POST",
                        headers: {
                            "accept": "application/json"
                        },
                        body: null
                    });
                    const maneuverDronesHold = await maneuverDronesResponse.json();
                    setManeuverDrones(maneuverDronesHold.Drones || []);
                } catch (error) {
                    console.error("Error fetching data:", error);
                }
            } else {
                setManeuverDrones([]);
            }
        };

        fetchManeuverDrones();
    }, [selectedManeuver]);

    const handleDroneSelect = (drone) => {
        setSelectedDrone(drone);
    };

    const handleManeuverSelect = (maneuver) => {
        setSelectedManeuver(maneuver);
    };

    return (
        <div style={{ position: "relative", width: "100vw", height: "100vh" }}>
            <div style={{
                position: "absolute",
                left: "20%",
                top: "50%",
                transform: "translate(-50%, -50%)",
                padding: "20px",
                borderRadius: "8px",
            }}>
                <DroneList drones={drones} onDroneSelect={handleDroneSelect} selectedDrone={selectedDrone} maneuverDrones={maneuverDrones}/>
            </div>
            <div style={{
                position: "absolute",
                left: "20%",
                top: "80%",
                transform: "translate(-50%, -50%)",
                padding: "20px",
                borderRadius: "8px",
            }}>
                <ArmButton selectedDrone={selectedDrone}/>
            </div>
            <div className="map-container" style = {{
                display: "flex",
                flexDirection: 'column',
                justifyContent: "center",
                alignItems: "center",
                height: "100vh",
                width: "100vw",

            }}>
                <MapComponent drones={drones} selectedDrone={selectedDrone}/>

                
            </div>
            <div className="gauges-container" style={{
                position: "absolute",
                left: "50%",
                top: "87%",
                transform: "translate(-50%, -50%)", 
            }}>
                <AltimeterGauge selectedDrone={selectedDrone}/>
            </div>
            <div style={{
                position: "absolute",
                left: "80%",
                top: "50%",
                transform: "translate(-50%, -50%)",
                padding: "20px",
                borderRadius: "8px",
            }}>
                <ManeuverList maneuvers={maneuvers} onManeuverSelect={handleManeuverSelect} selectedManeuver={selectedManeuver}/>
            </div>
            
        </div>
    );
}

export default HomeScreen;