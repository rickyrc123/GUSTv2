import PropTypes from 'prop-types';
const ArmButton = ({ selectedDrone }) => {
    
    const handleClick = async () => {
        try{
            await fetch(`http://localhost:8000/droens/single_connection/take_off?${selectedDrone.current_alt}`);
        } catch (err) {
            console.error('Failed to arm drone', err)
        }
        
    };
    return(
        <button style={{}} onClick={handleClick}>
            {"ARM"}
        </button>
    );
}

ArmButton.propTypes = {
    selectedDrone: PropTypes.shape({
                name: PropTypes.string,
                model: PropTypes.string,
                current_lat: PropTypes.number,
                current_long: PropTypes.number,
                current_alt: PropTypes.number,
                current_yaw: PropTypes.number
    }),
}

export default ArmButton