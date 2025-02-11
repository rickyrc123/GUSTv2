import { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import {AttitudeIndicator, HeadingIndicator} from 'react-flight-indicators';

const NavBall = ({ droneID }) => {
    const [attitude, setAttitude] = useState({pitch: 0, roll: 0, heading: 0});

    useEffect(() => {
        if (!droneID) return;

        const fetchAttitude = async () => {
            try {
                const response = await fetch(`/info?droneID=${droneID}`);
                const data = await response.json();

                setAttitude({pitch: data.pitch ?? 0, roll: data.roll ?? 0, heading: data.heading ?? 0});
            } catch (error) {
                console.error(`Error fetching attitude data from drone ${droneID}`, error);
            }
        };

        fetchAttitude();
    }, [droneID]);

    const {pitch, roll, heading} = attitude;

    return (
        <div style={{ display: 'flex', gap: '2rem'}}>
            <AttitudeIndicator pitch={pitch} roll={roll} size={200}/>
            <HeadingIndicator heading={heading} size={200}/>
        </div>
    );
};

NavBall.propTypes = {
    droneID: PropTypes.string.isRequired,
};

export default NavBall;