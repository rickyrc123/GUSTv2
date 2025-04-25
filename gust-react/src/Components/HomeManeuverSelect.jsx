import PropTypes from "prop-types";
import { FixedSizeList as List } from "react-window";

const ManeuverList = ({ maneuvers = [], height = 575, width = 180, itemSize = 75, onManeuverSelect, selectedManeuver })=> {
    
    const Row = ({ index }) => {
        const handleClick = () => {
            onManeuverSelect(maneuvers[index]);
        };

        //First div style is how the buttons fit in the list
        return (
            <div style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                marginBottom: '15px'
            }}>    
                <button style={{width: '90%', background: selectedManeuver && selectedManeuver === maneuvers[index] ? '#2196f3' : '#8bcafd'}} onClick={handleClick}>
                    {maneuvers[index]}
                </button>
            </div>
        );
    };


    return(
        <div style={{ 
            border: "3px solid #ddd",
            borderColor: "#a0a0a0",
            borderRadius: "8px", 
            overflow: "hidden",
            backgroundColor: "#b0b0b0"
        }}>
            <List
                itemSize={itemSize}
                itemCount={maneuvers.length}
                height={height}
                width={width}
            >
                {Row}
            </List>  
        </div>
    );
};

ManeuverList.propTypes = {
    height: PropTypes.number,
    width: PropTypes.number,
    itemSize: PropTypes.number,
    index: PropTypes.any,
    onManeuverSelect: PropTypes.func.isRequired,
    maneuvers: PropTypes.array,
    selectedManeuver: PropTypes.string
};

export default ManeuverList;