import PropTypes from "prop-types";
import { FixedSizeList as List } from "react-window";

const DroneList = ({
    drones = [],
    height = 575,
    width = 180,
    itemSize = 75,
    onDroneSelect,
    selectedDrone,
    maneuverDrones = []
}) => {
    const filteredDrones = drones.filter((drone) => maneuverDrones.includes(drone.name));

    const Row = ({ index }) => {
        if(!maneuverDrones.length){
            return;
        }
        const drone = filteredDrones[index];

        const handleClick = () => {
            onDroneSelect(drone);
        };

        return (
            <div
                style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                marginBottom: "15px"
                }}
            >
                <button
                    style={{
                        width: "90%",
                        background:
                        selectedDrone && selectedDrone.name === drone.name
                            ? "#2196f3"
                            : "#8bcafd"
                    }}
                    onClick={handleClick}
                >
                    {drone.name}
                </button>
            </div>
            );
    };

    return (
        <div
        style={{
            border: "1px solid #ddd",
            borderRadius: "8px",
            overflow: "hidden"
        }}
        >
        <List
            itemSize={itemSize}
            itemCount={filteredDrones.length}
            height={height}
            width={width}
        >
            {Row}
        </List>
        </div>
    );
};

DroneList.propTypes = {
  height: PropTypes.number,
  width: PropTypes.number,
  itemSize: PropTypes.number,
  onDroneSelect: PropTypes.func.isRequired,
  drones: PropTypes.array,
  maneuverDrones: PropTypes.array,
  selectedDrone: PropTypes.any,
  index: PropTypes.any
};

export default DroneList;
