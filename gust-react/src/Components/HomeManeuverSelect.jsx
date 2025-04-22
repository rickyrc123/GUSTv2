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
            border: "1px solid #ddd", 
            borderRadius: "8px", 
            overflow: "hidden"
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