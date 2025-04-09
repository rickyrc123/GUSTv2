import MapComponent from "./MapComponent.jsx";
import DroneList from "./DroneSelection.jsx";
import AltimeterGauge from "./AltimeterGauge.jsx";
import HomeManeuverSelect from "./HomeManeuverSelect.jsx";
import { useState, useEffect } from "react";

function HomeScreen() {
    const [selectedDrone, setSelectedDrone] = useState(null);
    const [drones, setDrones] = useState([]);

    
  
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch("http://localhost:8000/drones");
                const data = await response.json();
                setDrones(data.Drones || []);
            } catch (error) {
                console.error("Error fetching data:", error);
            }
        };

        fetchData();
        const interval = setInterval(fetchData, 1000);
        return () => clearInterval(interval);
    }, []);

    const handleDroneSelect = (drone) => {
        setSelectedDrone(drone);
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
                <DroneList drones={drones} onDroneSelect={handleDroneSelect}/>
                <HomeManeuverSelect placeholder={"Maneuvers"}/>
            </div>
            <div className="map-container" style = {{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                height: "100vh",
                width: "100vw",
            }}>
                <MapComponent drones={drones} selectedDrone={selectedDrone}/>
            </div>
            <div className="gauges-container" style={{
                position: "absolute",
                left: "82%",
                top: "50%",
                transform: "translate(-50%, -50%)",
                padding: "20px",
                borderRadius: "8px",
            }}>
                <AltimeterGauge selectedDrone={selectedDrone}/>
            </div>
        </div>
    );
}

export default HomeScreen;