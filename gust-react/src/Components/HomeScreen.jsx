import MapComponent from "./MapComponent.jsx";
import DroneList from "./DroneSelection.jsx";
//import { useState, useEffect } from "react";

function HomeScreen() {
    // const [items, setItems] = useState([]);
  
    // useEffect(() => {
    //     const fetchData = async () => {
    //         try {
    //             const response = await fetch("http://localhost:8000/drones");
    //             const data = await response.json();
    //             console.log("Drone:", response.Dones);          
    //             setItems(data.Drones);
    //         } catch (error) {
    //             console.error("Error fetching data:", error);
    //         }
    // };
    //           fetchData();
    //           const interval = setInterval(fetchData, 500);
    //           return () => clearInterval(interval);
  
    // }, []);

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
                <DroneList />
            </div>
            <div style = {{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                height: "100vh",
                width: "100vw",
            }}>
                <MapComponent />
            </div>
        </div>
    );
}

export default HomeScreen;