import PlanningWidget from './PlanningWidget'
function PlanningScreen() {
    return (
        <div style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            height: "100vh",
            width: "100vw",
          }}>
            <PlanningWidget />
        </div>
    );
}

export default PlanningScreen;