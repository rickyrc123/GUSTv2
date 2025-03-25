import { useState, useEffect } from "react";
import PropTypes from "prop-types";
import { FixedSizeList as List } from "react-window";

const DroneList = ({ height = 575, width = 180, itemSize = 75 })=> {
    const [items, setItems] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {

                const response = await fetch("http://localhost:8000/drones");
                const data = await response.json();
                console.log("Drone:", data.Drones)
                
                setItems(data.Drones);
            } catch (error) {
                console.error("Error fetching data:", error);
            }
        };

        fetchData();

        //refresh every 1 second (1000ms)
        const interval = setInterval(fetchData, 1000);
        return () => clearInterval(interval);
    }, []);
    
    const Row = ({ index }) => {
        const handleClick = () => {
            alert(`Name:  ${items[index].name}          \n
                    lat:  ${items[index].current_long}  \n
                   long:  ${items[index].current_lat}   \n
                    alt:  ${items[index].current_alt}   \n
                    yaw:  ${items[index].current_yaw}   \n`);

            //TODO highlight clicked drone on map
        };

        //First div style is how the buttons fit in the list
        return (
            <div style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                marginBottom: '15px'
            }}>    
                <button style={{width: '90%'}} onClick={handleClick}>
                    {items[index].name}
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
                itemCount={items.length}
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
    style: PropTypes.any
};

export default DroneList;