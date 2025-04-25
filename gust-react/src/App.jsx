import HomeScreen from "./Components/HomeScreen.jsx";
import PlanningScreen from "./Components/PlanningScreen.jsx";
import ConnectionScreen from "./Components/ConnectionScreen.jsx";
import { useState } from "react";


function App() {
  const [screen, setScreen] = useState("home");
  return (
    <div>
        <nav style={{
              position: "absolute",
              top: 0, 
              left: 0, 
              display: "flex",
              gap: "10px",
              padding: "10px",
              zIndex: 1000
          }}>
              <button onClick={() => setScreen("home")}>Home</button>
              <button onClick={() => setScreen("planning")}>Planning</button>
              <button onClick={() => setScreen("connection")}>Connection</button>
        </nav>
        {screen === "home" && <HomeScreen />}
        {screen === "planning" && <PlanningScreen />}
        {screen === "connection" && <ConnectionScreen />}
    </div>
  );
}


export default App;
