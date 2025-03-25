import PropTypes from 'prop-types';
import React, { useEffect, useState } from 'react';
import { GaugeComponent } from 'react-gauge-component';

const AltimeterGauge = ({ droneID }) => {
    const [altitude, setAltitude] = useState(0);

    useEffect(() => {
        if (!droneID) return;

        const fetchAltitude = async () => {
            try {
                const response = await fetch(`http://localhost:8000/drones/positions?drone_id=${droneID}`);
                const data = await response.json();
                setAltitude(data.altitude || 0);
            } catch (error) {
                console.error(`Error fetching altitude from drone: ${droneID}`, error);
            }
        }

        fetchAltitude();
        const interval = setInterval(fetchData, 500);
        return () => clearInterval(interval);

    }, [droneID]);

    return (
        <div style={{ width: 300, margin: '0 auto'}}>
            <GaugeComponent
                value={altitude}
                max={5000}
                label="Altitude"
                color="#FF5722"
                backgroundColor="#ECECEC"
                height={250}
                width={250}
            />
        </div>
    );
}

AltimeterGauge.propTypes = {
    droneID: PropTypes.string
};

export default AltimeterGauge;