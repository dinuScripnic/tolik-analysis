import React, { useState, useEffect } from 'react';
import axios, { AxiosResponse } from 'axios';
import { API_URL } from '../config';
import { useAlertMessages, ErrorMessage } from '../components/AlertMessages';
import { Evaluation } from '../types/evaluation';
import { Result } from '../types/results';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch } from '@fortawesome/free-solid-svg-icons';

interface SearchBarProps {
    responseType: 'result' | 'evaluation';
    onDataFetched: (data: Evaluation[] | Result) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ responseType, onDataFetched }: SearchBarProps) => {
    const {
        errorMessage,
        closeErrorMessage,
        handleErrorMessage,
    } = useAlertMessages();
    const [isLoading, setIsLoading] = useState(false);
    const [facultyJSON, setFacultyJSON] = useState<any>({});
    const [facultiesList, setFacultyList] = useState<string[]>([]);
    const [searchTerm, setSearchTerm] = useState<string>('');
    const [suggestions, setSuggestions] = useState<string[]>([]);
    const [filteredSuggestions, setFilteredSuggestions] = useState<string[]>([]);
    const [selectedFaculty, setSelectedFaculty] = useState<string>('');

    const setSearchData = (data: string[], faculty: string) => {
        setSuggestions(data);
        setFilteredSuggestions(data);
        setSelectedFaculty(faculty);
    }

    useEffect(() => {
        // Fetch faculties and their courses when the component mounts
        const fetchFaculties = async () => {
            setIsLoading(true);
            try {
                const response = await axios.get(`${API_URL}/faculties/list`);
                const { data } = response;
                const faculties = Object.keys(data);
                setFacultyList(faculties);
                setFacultyJSON(data);
                setSearchData(data[faculties[0]], faculties[0]);
            }
            catch (error) {
                handleErrorMessage(`Error fetching faculties and courses: ${error}`);
            } finally {
                setIsLoading(false);
            }
        };
        fetchFaculties();
    }
        , []);

    const handleFacultyChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        const faculty = event.target.value;
        const courses = facultyJSON[faculty];
        setSearchData(courses, faculty);
    }

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const inputValue = event.target.value;
        setSearchTerm(inputValue);
        const filtered = suggestions.filter((item) =>
            item.toLowerCase().includes(inputValue.toLowerCase())
        );
        setFilteredSuggestions(filtered);
    };

    const handleSelectItem = async (item: string): Promise<void> => {
        setIsLoading(true);
        try {
            let response;
            if (responseType === 'result') {
                response = await axios.get<Result>(`${API_URL}/results/course/${item}`);
            } else if (responseType === 'evaluation') {
                response = await axios.get<Evaluation[]>(`${API_URL}/evaluations/course/${item}`);
            }
            const responseData = (response as AxiosResponse<Result | Evaluation[]>).data;
            onDataFetched(responseData);
            setSearchTerm('');
            setFilteredSuggestions([]);
        } catch (error) {
            handleErrorMessage(`Error fetching data: ${error}`);
        } finally {
            setIsLoading(false);
        }
    }

    return (
        <div className="relative flex flex-grow">
            {/* Display error message */}
            {errorMessage && (
                <ErrorMessage message={errorMessage} onClose={closeErrorMessage} />
            )}
            <div className="dropdown flex-grow">
                <div className="relative">
                    <div className="border rounded-lg flex items-center">
                        <select
                            className="pl-2 pr-2 bg-transparent border-r outline-none"
                            value={selectedFaculty}
                            onChange={handleFacultyChange}
                        >
                            {
                                facultiesList.map((faculty) => (
                                    <option key={faculty} value={faculty} className='bg-black'>
                                        {faculty}
                                    </option>
                                ))
                            }
                        </select>
                        <input
                            type="text"
                            placeholder={`Search for couse...`}
                            value={searchTerm}
                            onChange={handleInputChange}
                            className="input px-3 py-2 w-full outline-none bg-transparent"
                        />
                        <FontAwesomeIcon icon={faSearch} className="mr-5" />
                    </div>

                    {isLoading ? (
                        <div className="absolute inset-0 flex items-center justify-center">
                            <div className="spinner-border text-blue-500"></div>
                        </div>
                    ) : filteredSuggestions.length > 0 && (
                        <ul className="suggestions-list absolute flexx z-50 bg-opacity-50 rounded border divide-y w-full">
                            {filteredSuggestions.map((item, index) => (
                                <li
                                    key={index}
                                    onClick={() => handleSelectItem(item)}
                                    className="cursor-pointer p-2 transition-colors bg-black bg-opacity-75 hover:bg-gray-400 hover:bg-opacity-1 hover:text-black"
                                >
                                    {item}
                                </li>
                            ))}
                        </ul>
                    )}
                </div>
            </div>
        </div >
    );
};

export default SearchBar;
