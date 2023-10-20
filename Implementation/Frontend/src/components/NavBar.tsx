import React from 'react';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faHome, faFileUpload, faSearch, faChartBar } from '@fortawesome/free-solid-svg-icons';

const Navbar: React.FC = () => {
    return (
        <nav className="bg-blue-500 p-4 sticky top-1">
            <div className="container mx-auto flex justify-center">
                <ul className="flex space-x-4 items-center">
                    <li className="text-white text-sm text-center transition-transform hover:scale-110 hover:text-yellow-500 pr-5">
                        <Link to="/">
                            <FontAwesomeIcon icon={faHome} className="text-2xl" />
                            <div>Home</div>
                        </Link>
                    </li>
                    <li className="text-white text-sm text-center transition-transform hover:scale-110 hover:text-yellow-500 pr-5">
                        <Link to="/upload_evaluations">
                            <FontAwesomeIcon icon={faFileUpload} className="text-2xl" />
                            <div>Upload Evaluations</div>
                        </Link>
                    </li>
                    <li className="text-white text-sm text-center transition-transform hover:scale-110 hover:text-yellow-500 pr-5">
                        <Link to="/search_evaluations">
                            <FontAwesomeIcon icon={faSearch} className="text-2xl" />
                            <div>Search Evaluations</div>
                        </Link>
                    </li>
                    <li className="text-white text-sm text-center transition-transform hover:scale-110 hover:text-yellow-500">
                        <Link to="/dashboard">
                            <FontAwesomeIcon icon={faChartBar} className="text-2xl" />
                            <div>Dashboard</div>
                        </Link>
                    </li>
                </ul>
            </div>
        </nav>
    );
};

export default Navbar;
