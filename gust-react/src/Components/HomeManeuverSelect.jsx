import PropTypes from "prop-types";
import { useState, useRef, useEffect } from 'react';

const HomeManeuverSelect = ({placeholder}) => {
    const [isOpen, setIsOpen] = useState(false);
    const [selected, setSelected] = useState(null);
    const dropdownRef = useRef(null);

    const toggle = () => setIsOpen(!isOpen);

    const selectOption = (option) => {
        setSelected(option);
        setIsOpen(false);
    };

    const options = [
        { value: '1', label: 'Option 1' },
        { value: '2', label: 'Option 2' },
        { value: '3', label: 'Option 3' }
      ];

    useEffect(() => {
        const handleClickOutside = (e) => {
        if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
            setIsOpen(false);
        }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    return (
        <div ref={dropdownRef} style={{ position: 'relative', display: 'inline-block' }}>
        <div onClick={toggle} style={{ cursor: 'pointer', padding: '8px', border: '1px solid #ccc', color: '#000' }}>
            {selected ? selected.label : placeholder}
        </div>
        {isOpen && (
            <div style={{ position: 'absolute', top: '100%', left: 0, right: 0, border: '1px solid #ccc' }}>
            {options.map((option) => (
                <div 
                key={option.value} 
                onClick={() => selectOption(option)}
                style={{ padding: '8px', cursor: 'pointer', backgroundColor: '#fff', color: '#000' }}
                >
                {option.label}
                </div>
            ))}
            </div>
        )}
        </div>
    );
};


HomeManeuverSelect.propTypes = {
    placeholder: PropTypes.any,
}

export default HomeManeuverSelect;