import React from "react";
import MapComponent from "./Components/MapComponent.jsx";
import DroneList from "./ListComponent";


function App() {
  return (
    <div style = {{
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      height: "100vh",
      width: "100vw",
    }}>
      
    <MapComponent />
    <DroneList />
    </div>
    
  );
}


export default App;
