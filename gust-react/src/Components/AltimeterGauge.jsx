import PropTypes from 'prop-types';
import { GaugeComponent } from 'react-gauge-component';

const AltimeterGauge = ({ selectedDrone }) => {
    
    let altitude = 0;

    if(selectedDrone){
        altitude = selectedDrone.current_alt;
    }
    return (
        <div style={{ width: 300, margin: '0 auto'}}>
            <GaugeComponent
                arc={{
                    subArcs: [
                      {
                        limit: 200,
                        showTick: true
                      },
                      {
                        limit: 400,
                        showTick: true
                      },
                      {
                        limit: 600,
                        showTick: true
                      },
                      {
                        limit: 800,
                        showTick: true
                      },
                      {
                        limit: 1000,
                        showTick: true
                      },
                    ]
                }}
                value={altitude}
                minValue={0}
                maxValue={1000}
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