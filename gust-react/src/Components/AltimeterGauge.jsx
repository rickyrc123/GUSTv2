import PropTypes from 'prop-types';
import { GaugeComponent } from 'react-gauge-component';

const AltimeterGauge = ({ selectedDrone }) => {
    
    let altitude = 0;

    if(selectedDrone){
        altitude = selectedDrone.current_alt;
    }

    const addFt = (value) => {
        return value + ' ft.'
    }

    return (
        <GaugeComponent
            arc={{
                width: 0.2,
                colorArray: ["#2196f3"],
                subArcs: [{ limit: 200, showTick: true}, {limit: 400, showTick: true}, {limit: 600, showTick: true}, {limit: 800, showTick: true}, {limit: 1000, showTick: true},],
            }}
            value={altitude}
            valueFormatter={(value) => `${value} ft.`}
            minValue={0}
            maxValue={1000}
            style={{
                width: 300
            }}
            labels={{
                valueLabel: {
                    style: {fontSize: 40},
                    formatTextValue: addFt
                    }
            }}
            color="#2196f3"
            backgroundColor="#2196f3"
        />
    );
}

AltimeterGauge.propTypes = {
    selectedDrone: PropTypes.shape({
            name: PropTypes.string,
            model: PropTypes.string,
            current_lat: PropTypes.number,
            current_long: PropTypes.number,
            current_alt: PropTypes.number,
            current_yaw: PropTypes.number
        }),
};

export default AltimeterGauge;