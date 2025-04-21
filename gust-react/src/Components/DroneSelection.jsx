import PropTypes from "prop-types";
import { FixedSizeList as List } from "react-window";

const DroneList = ({ drones = [], height = 575, width = 180, itemSize = 75, onDroneSelect, selectedDrone })=> {
    
    const Row = ({ index }) => {
        const handleClick = () => {
            onDroneSelect(drones[index]);
        };

        //First div style is how the buttons fit in the list
        return (
            <div style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                marginBottom: '15px',
                
            }}>    
                <button style={{width: '90%', background: selectedDrone && selectedDrone.name === drones[index].name ? '#2196f3' : 'red'}} onClick={handleClick} >
                    {drones[index].name}
                </button>
            </div>
        );
    };


    return(
        <div style={{ 
            border: "1px solid #ddd", 
            borderRadius: "8px", 
            overflow: "hidden"
        }}>
            <List
                itemSize={itemSize}
                itemCount={drones.length}
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
    index: PropTypes.any,
    onDroneSelect: PropTypes.func.isRequired,
    drones: PropTypes.array,
    selectedDrone: PropTypes.any
};

export default DroneList;