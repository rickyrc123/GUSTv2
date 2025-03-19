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
                
                
                setItems(data.Drones);
            } catch (error) {
                console.error("Error fetching data:", error);
            }
        };

        fetchData();

    }); 

    //hold before we get the CORS conenction
    const test = [
        { name: 'Item 1', action: 'Action 1' },
        { name: 'Item 2', action: 'Action 2' },
        { name: 'Item 3', action: 'Action 3' },
        { name: 'Item 4', action: 'Action 4' },
        { name: 'Item 5', action: 'Action 5' },
      ];
    
    const Row = ({ index }) => {
        const handleClick = () => {
            alert(`You clicked on: ${items[index].action}`);
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
                    {test[index].name}
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
                itemCount={test.length}
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