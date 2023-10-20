import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTimes } from '@fortawesome/free-solid-svg-icons';

interface SuccessMessageProps {
    message: string | null;
    onClose: () => void;
}

export const SuccessMessage: React.FC<SuccessMessageProps> = ({ message, onClose }) => {
    return (
        <div className="fixed top-16 left-1/2 transform -translate-x-1/2 w-1/2">
            <div className="bg-green-500 text-white p-4 rounded-md flex justify-between items-center">
                <span className='text-center'>{message}</span>
                <button
                    className="bg-white text-green-500 p-1 rounded-full hover:bg-green-100 justify-self-end"
                    onClick={onClose}
                >
                    <FontAwesomeIcon icon={faTimes} size='sm' />
                </button>
            </div>
        </div>
    );
};

interface ErrorMessageProps {
    message: string | null;
    onClose: () => void;
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({ message, onClose }) => {
    return (

        <div className="fixed top-16 left-1/2 transform -translate-x-1/2 w-1/2">
            <div className="bg-red-500 text-white p-4 rounded-md flex justify-between items-center">
                <span className='text-center'>{message}</span>
                <button
                    className="bg-white text-red-500 p-1 rounded-full hover:bg-red-100 justify-self-end"
                    onClick={onClose}
                >
                    <FontAwesomeIcon icon={faTimes} size='sm' />
                </button>
            </div>
        </div>
    );
};

export const useAlertMessages = () => {
    const [successMessage, setSuccessMessage] = useState<string | null>(null);
    const [errorMessage, setErrorMessage] = useState<string | null>(null);

    const closeErrorMessage = () => {
        setErrorMessage(null);
    };

    const closeSuccessMessage = () => {
        setSuccessMessage(null);
    };

    const handleSuccessMessage = (message: string | null) => {
        setSuccessMessage(message);
        setErrorMessage(null);

        setTimeout(() => {
            setSuccessMessage(null);
        }, 10000);
    };

    const handleErrorMessage = (message: string | null) => {
        setSuccessMessage(null);
        setErrorMessage(message);

        setTimeout(() => {
            setErrorMessage(null);
        }, 10000);
    };

    return {
        successMessage,
        errorMessage,
        closeErrorMessage,
        closeSuccessMessage,
        handleSuccessMessage,
        handleErrorMessage,
    };
};
