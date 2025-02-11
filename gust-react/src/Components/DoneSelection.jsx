import { useState, useEffect } from "react";
import PropTypes from "prop-types";
import { FixedSizeList as List } from "react-window";

const DroneList = ({ apiEndpoint, height = 300, width = 300, itemSize = 35 })=> {
    const [items, setItems] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(apiEndpoint);
                const data = await response.json();
                setItems(data);
            } catch (error) {
                console.error("Error fetching data:", error);
            }
        };

        fetchData();

    }, [apiEndpoint]); 

    
    const renderRow = ({index, style}) => (
        <div style={}>
            {items[index]}
        </div>
    );

    return(
        <div style={}>
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