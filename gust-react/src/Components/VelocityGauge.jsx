import { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import { Gauge } from 'react-gauge-component';

const VelocityGauge = ({ droneID }) => {
    const [velocity, setVelocity] = useState(0);

    useEffect(() => {
        if (!droneID) return;

        const fetchVelocity = async () => {
            try {
                const response = await fetch(`/info?droneID=${droneID}`);
                const data = await response.json();
                setVelocity(data.Velocity || 0);
            } catch (error) {
                console.error(`Error fetching velocity from drone: ${droneID}`, error);
            }
        }

        fetchVelocity();
    }, [droneID]);
    return (
        <div style={{ width: 300, margin: '0 auto'}}>
            <Gauge
                value={velocity}
                max={20}
                label="Velocity (m/s)"
                color="#FF5722"
                backgroundColor="#ECECEC"
                height={250}
                width={250}
            />
        </div>
    );
}

VelocityGauge.propTypes = {
    droneID: PropTypes.string.isRequired,
};

export default VelocityGauge;