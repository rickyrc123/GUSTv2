import MapComponent from "./MapComponent.jsx";
import DroneList from "./DroneSelection.jsx";
import AltimeterGauge from "./AltimeterGauge.jsx";
import './HomeScreen.css';
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
        <div className="HomeScreen">
            <div className='drone-list-container'>
                <DroneList drones={drones} onDroneSelect={handleDroneSelect}/>
            </div>
            <div className="map-container">
                <MapComponent drones={drones} selectedDrone={selectedDrone}/>
            </div>
            <div className="gauges-container">
                <AltimeterGauge selectedDrone={selectedDrone}/>
            </div>
        </div>
    );
}

export default HomeScreen;