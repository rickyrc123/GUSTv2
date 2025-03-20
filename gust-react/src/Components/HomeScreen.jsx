import MapComponent from "./MapComponent.jsx";
import DroneList from "./DroneSelection.jsx";

function HomeScreen() {
    return (
    <div style={{ position: "relative", width: "100vw", height: "100vh" }}>
      <div
        style={{
          position: "absolute",
          left: "20%",
          top: "50%",
          transform: "translate(-50%, -50%)",
          padding: "20px",
          borderRadius: "8px",
        }}
      >
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