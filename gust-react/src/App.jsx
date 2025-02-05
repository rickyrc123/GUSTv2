import React from "react";
import MapComponent from "./Components/MapComponent.jsx";

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
    </div>
  );
}


export default App;
