import React, { useEffect, useState } from 'react';
import { Gauge } from 'react-gauge-component';

const AltimeterGauge = ({ droneID }) => {
    const [altitude, setAltitude] = useState(0);

    useEffect(() => {
        if (!droneID) return;

        const fetchAltitude = async () => {
            try {
                const response = await fetch(`/info?droneID=${droneID}`);
                const data = await response.json();
                setAltitude(data.altitude || 0);
            } catch (error) {
                console.error(`Error fetching altitude from drone: ${droneID}`, error);
            }
        }

        fetchAltitude();
    }, [droneID]);
    return (
        <div style={{ width: 300, margin: '0 auto'}}>
            <Gauge
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