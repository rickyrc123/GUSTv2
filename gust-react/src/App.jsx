import MapComponent from "./Components/MapComponent.jsx";
import DroneList from "./Components/DroneSelection.jsx";


function App() {
  return (
    <div style = {{
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      height: "100vh",
      width: "100vw",
    }}>
    
    <DroneList />
    <MapComponent />
    
    </div>
    
  );
}


export default App;
