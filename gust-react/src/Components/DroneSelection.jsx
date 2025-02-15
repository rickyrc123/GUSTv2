import { useState, useEffect } from "react";
import PropTypes from "prop-types";
import { FixedSizeList as List } from "react-window";

const DroneList = ({ apiEndpoint, height = 300, width = 300, itemSize = 35 })=> {
    const [items, setItems] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {

                const response = await fetch("http://localhost:8000/drones", {
                    
                });
                const data = await response.json();
                console.log("API Response", data)
                const drones = JSON.parse(data.Drones).data;
                setItems(drones);
            } catch (error) {
                console.error("Error fetching data:", error);
            }
        };

        fetchData();

    }, [apiEndpoint]); 

    
    const renderRow = ({index, style}) => (
        <div style={{ 
            ...style, 
            padding: "10px", 
            borderBottom: "1px solid #ccc",
            backgroundColor: index % 2 === 0 ? "#f9f9f9" : "#fff" 
        }}>
            {items[index].name}
            
        </div>
    );

    return(
        <div style={{ 
            border: "1px solid #ddd", 
            borderRadius: "8px", 
            overflow: "hidden",
            width: `${width}px`
        }}>
            <List
                itemSize={itemSize}
                itemCount={items.length}
                height={height}
                width={width}
            >
                {renderRow}
            </List>  
        </div>
    );
};

DroneList.propTypes = {
    apiEndpoint: PropTypes.string.isRequired,
    height: PropTypes.number,
    width: PropTypes.number,
    itemSize: PropTypes.number,
};

export default DroneList;