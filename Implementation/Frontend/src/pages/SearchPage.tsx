import React, { useState } from 'react';
import SearchBar from '../components/GeneralSearchBar';
import { Evaluation } from '../types/evaluation';
import ComputerImage from '../assets/computer.jpg'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTimes } from '@fortawesome/free-solid-svg-icons';

const SearchPage: React.FC = () => {
    const [fetchedData, setFetchedData] = useState<Evaluation[]>([]);

    const handleDataFetched = (data: Evaluation[]) => {
        setFetchedData(data);
    };


    const toggleModal = (index: string) => {
        const modal = document.getElementById(index) as HTMLDialogElement;
        if (modal) {
            modal.showModal();
        }
    }

    return (
        <div>
            <div className="flex flex-wrap mx-auto max-w-screen justify-center pt-5 w-1/3">
                <SearchBar responseType="evaluation" onDataFetched={handleDataFetched} />{/*solve this error, even tho all works*/}
            </div>
            <div className="flex flex-wrap justify-center mx-auto max-w-screen w-3/4">
                {fetchedData.length === 0 ? (
                    // TODO: Make it more nice
                    <p>No data available.</p>
                ) : (fetchedData.map((evaluation, index) => (
                    <div className="w-full sm:w-1/2 md:w-1/2 lg:w-1/4 mb-4 p-5" key={index}>
                        <div className="card bg-base-100 shadow-xl image-full">
                            <figure>
                                <img src={ComputerImage} alt="Evaluation" className="rounded-t-lg" />
                            </figure>
                            <div className="card-body">
                                <h2 className="card-title text-lg sm:text-xl md:text-2xl lg:text-lg">
                                    {evaluation.semester} - {evaluation.course}
                                </h2>
                                <p>
                                    <strong>Semester:</strong> {evaluation.semester}<br />
                                    <strong>Faculty:</strong> {evaluation.faculty}<br />
                                    <strong>Course:</strong> {evaluation.course}<br />
                                    <strong>Cohort:</strong> {evaluation.cohort}<br />
                                    <strong>Lecturer:</strong> {evaluation.lecturer}
                                </p>
                                <div className="card-actions justify-center">
                                    <button
                                        className="btn btn-outline btn-info btn-sm"
                                        onClick={() => toggleModal(String(index))}
                                    >
                                        See Evaluations
                                    </button>
                                </div>
                            </div>
                        </div>
                        <dialog id={String(index)} className="modal">
                            <div className="modal-box max-w-max w-3/4">
                                <form method="dialog">
                                    <button className="btn btn-sm btn-circle btn-ghost hover:bg-red-500 absolute right-2 top-2 mt-4 mb-3">
                                        <FontAwesomeIcon icon={faTimes} />
                                    </button>
                                </form>
                                <div className="flex flex-wrap mx-auto justify-center max-w-max pb-2">
                                    <h1 className="font-bold text-xl pt-2 pb-2">Evaluation Details</h1>
                                </div>
                                <hr className="border-gray-400 pb-4" />
                                {evaluation.evaluations.map((evaluation, index) => (
                                    <div className="collapse collapse-plus border pt-1 my-4" key={index}>
                                        <input type="checkbox" name="my-accordion-3" />
                                        <div className="collapse-title text-xl font-medium">
                                            Evaluation {index + 1}
                                        </div>
                                        <div className="collapse-content">

                                            {
                                                evaluation.split('\n').map((item) => {
                                                    return <p className='pb-1.5 indent-4'>{item}</p>
                                                })
                                            }
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </dialog>
                    </div>
                )))}
            </div>

        </div>
    );
};

export default SearchPage;
