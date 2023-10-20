import React, { useState, useRef } from 'react';
import { API_URL } from '../config';
import { useAlertMessages, SuccessMessage, ErrorMessage } from '../components/AlertMessages';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTrash, faPlus, faTimes } from '@fortawesome/free-solid-svg-icons';


const SubmitPage: React.FC = () => {
    const {
        successMessage,
        errorMessage,
        closeSuccessMessage,
        closeErrorMessage,
        handleSuccessMessage,
        handleErrorMessage,
    } = useAlertMessages();
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [evaluations, setEvaluations] = useState<{ id: number; value: string }[]>([{ id: 1, value: '' }]);
    const fileInputRef = useRef<HTMLInputElement | null>(null);

    const handleFileInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];

        // Check if the selected file is a JSON file
        if (file && file.type === 'application/json') {
            setSelectedFile(file);
        } else {
            alert('Please select a valid JSON file.');
        }
    };

    const handleFileUpload = async () => {
        if (!selectedFile) {
            alert('Please select a file.');
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const response = await fetch(`${API_URL}/evaluation/file`, {
                method: 'POST',
                body: formData,
            });
            console.log(response.status);

            if (response.status === 201) {
                handleSuccessMessage('File uploaded successfully!');
            } else if (response.status === 422) {
                handleErrorMessage('Error! Invalid JSON file.');
            } else {
                handleErrorMessage('Error! File upload failed.');
            }
        } catch (error) {
            console.error('Error uploading file:', error);
            handleErrorMessage('API Error! Could not access the API.');
        }
    };

    const handleAddEvaluation = () => {
        const newEvaluationId = evaluations.length + 1;
        setEvaluations([...evaluations, { id: newEvaluationId, value: '' }]);
    };

    const handleRemoveEvaluation = (idToRemove: number) => {
        const updatedEvaluations = evaluations.filter((evaluation) => evaluation.id !== idToRemove);
        setEvaluations(updatedEvaluations);
    };

    const handleEvaluationInputChange = (index: number, value: string) => {
        const updatedEvaluations = [...evaluations];
        updatedEvaluations[index] = value;
        setEvaluations(updatedEvaluations);
    };

    const handleSubmitManual = async () => {
        // Gather data from form fields
        const semesterInput = document.getElementById('semester') as HTMLInputElement;
        const semester = semesterInput?.value.trim();

        const cohortInput = document.getElementById('cohort') as HTMLInputElement;
        const cohort = cohortInput?.value.trim();

        const facultyInput = document.getElementById('faculty') as HTMLInputElement;
        const faculty = facultyInput?.value.trim();

        const courseInput = document.getElementById('course') as HTMLInputElement;
        const course = courseInput?.value.trim();

        const lecturerInput = document.getElementById('lecturer') as HTMLInputElement;
        const lecturer = lecturerInput?.value.trim();


        // Check if any of the required fields are empty
        if (!semester || !cohort || !faculty || !course || !lecturer) {
            handleErrorMessage('Error! Please fill out all fields.');
            return;
        }

        const formData = {
            semester,
            cohort,
            faculty,
            course,
            lecturer,
            evaluations,
        };

        console.log(formData);
        try {
            const response = await fetch(`${API_URL}/evaluation/multiple`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            if (response.status === 201) {
                handleSuccessMessage('Evaluations submitted successfully!');
            } else {
                handleErrorMessage('Error! Could not submit evaluations.');
            }
        } catch (error) {
            // Handle network error
            console.error('Error:', error);
            handleErrorMessage('API Error! Could not access the API.')
        }
    };

    const toggleJSONModal = () => {
        const modal = document.getElementById('JsonSubmitModal') as HTMLDialogElement;
        modal.showModal();
    };

    const toggleManualModal = () => {
        const modal = document.getElementById('ManualSubmitModal') as HTMLDialogElement;
        modal.showModal();
    };

    return (
        <div className="flex flex-col">

            {/* Display success message */}
            {successMessage && (
                <SuccessMessage message={successMessage} onClose={closeSuccessMessage} />
            )}
            {/* Display error message */}
            {errorMessage && (
                <ErrorMessage message={errorMessage} onClose={closeErrorMessage} />
            )}
            <div className="mx-auto max-w-lg p-4 rounded-lg  flex flex-col items-center justify-center h-screen">
                <h1 className="text-3xl font-bold text-center mb-4">Submit New Evaluations</h1>
                <div className="text-center text-gray-600 mb-4">
                    Welcome to our evaluation submission platform. Here, you can submit evaluations for courses, providing valuable feedback to help improve the learning experience.
                </div>

                <hr className="my-4" />
                <div className="flex justify-center space-x-4">
                    <button
                        className="btn btn-primary"
                        onClick={toggleJSONModal}
                    >
                        Submit JSON File
                    </button>
                    <button
                        className="btn btn-success"
                        onClick={toggleManualModal}
                    >
                        Submit Manually
                    </button>
                </div>
            </div>




            <dialog id="JsonSubmitModal" className="modal">

                <div className="modal-box p-6">

                    <form method="dialog">
                        <button className="btn btn-sm btn-circle btn-ghost hover:bg-red-500 absolute right-2 top-2 mt-4 mb-3" >
                            <FontAwesomeIcon icon={faTimes} />
                        </button>
                    </form>

                    <h1 className="text-4xl font-bold mb-4 text-center">Submit VIA JSON File</h1>
                    <hr className="my-4 border-t border-gray-300 mb-5" />

                    <div className="form-control mx-auto max-w-md flex justify-center items-center mb-6">
                        <input
                            type="file"
                            className="file-input file-input-bordered w-full max-w-xs m-4 file-input-primary"
                            accept=".json"
                            onChange={handleFileInputChange}
                            ref={fileInputRef}
                            required
                        />
                    </div>

                    <div className="flex justify-center">
                        <button
                            className="btn btn-accent btn-md"
                            onClick={handleFileUpload}
                            disabled={!selectedFile}
                        >
                            Upload
                        </button>
                    </div>
                </div>
            </dialog>

            <dialog id="ManualSubmitModal" className="modal">
                <div className="modal-box w-11/12 max-w-5xl p-6">

                    <form method="dialog">
                        <button className="btn btn-sm btn-circle btn-ghost hover:bg-red-500 absolute right-2 top-2 mt-3 mb-3" >
                            <FontAwesomeIcon icon={faTimes} />
                        </button>
                    </form>

                    <h1 className="text-3xl font-bold text-center mb-4">Submit Manually</h1>
                    <hr className="my-4 border-t border-gray-300" />

                    <div className="mx-auto max-w-lg mb-4">
                        <label htmlFor="semester" className="block mb-1 text-lg font-semibold">Semester:</label>
                        <input
                            type="text"
                            id="semester"
                            className="w-full border rounded-lg py-2 px-3 focus:outline-none focus:border-blue-500"
                            placeholder="e.g., WS2022/23"
                            title='Enter the semester'
                            required
                        />
                    </div>
                    <div className="mx-auto max-w-lg mb-4">
                        <label htmlFor="cohort" className="block mb-1 text-lg font-semibold">Cohort:</label>
                        <input
                            type="text"
                            id="cohort"
                            className="w-full border rounded-lg py-2 px-3"
                            placeholder="e.g., BSc"
                            title='Enter the name of the cohort'
                            required
                        />
                    </div>
                    <div className="mx-auto max-w-lg mb-4">
                        <label htmlFor="faculty" className="block mb-1 text-lg font-semibold">Faculty:</label>
                        <input
                            type="text"
                            id="faculty"
                            className="w-full border rounded-lg py-2 px-3"
                            placeholder="e.g., Informatics"
                            title='Enter the name of the faculty'
                            required
                        />
                    </div>
                    <div className="mx-auto max-w-lg mb-4">
                        <label htmlFor="course" className="block mb-1 text-lg font-semibold">Course:</label>
                        <input
                            type="text"
                            id="course"
                            className="w-full border rounded-lg py-2 px-3"
                            placeholder="e.g., Programming I"
                            title='Enter the name of the course'
                            required
                        />
                    </div>
                    <div className="mx-auto max-w-lg mb-4">
                        <label htmlFor="lecturer" className="block mb-1 text-lg font-semibold">Lecturer:</label>
                        <input
                            type="text"
                            id="lecturer"
                            className="w-full border rounded-lg py-2 px-3"
                            placeholder="e.g., Deepak Dhungana"
                            title='Enter the name of the lecturer'
                            required
                        />
                    </div>
                    <div className="mx-auto max-w-lg mb-4">
                        <label htmlFor="evaluations" className="block mb-1 text-lg font-semibold flex justify-between items-center">
                            <span>Evaluations:</span>
                            <button
                                className="btn bg-blue-300 hover:bg-green-500 btn-sm text-white"
                                onClick={handleAddEvaluation}
                                title="Add Evaluation"
                            >
                                <FontAwesomeIcon icon={faPlus} />
                            </button>
                        </label>

                        {evaluations.map((evaluation, index) => (
                            <div key={evaluation.id} className="relative mb-4">
                                <div className="flex items-center">
                                    <textarea
                                        className="w-full border rounded-lg py-2 px-3 pl-10 focus:outline-none focus:border-blue-500 textarea-lg"
                                        placeholder="Enter evaluation..."
                                        title='Enter student evaluation'
                                        value={evaluation.value}
                                        onChange={(e) => handleEvaluationInputChange(index, e.target.value)}
                                    />
                                    <button
                                        className="btn hover:bg-red-500 btn-xs btn-circle btn-ghost absolute left-2 top-2 "
                                        title='Remove evaluation'
                                        onClick={() => handleRemoveEvaluation(evaluation.id)}
                                    >
                                        <FontAwesomeIcon icon={faTrash} />
                                    </button>
                                </div>
                            </div>
                        ))}
                        {/* <button
                            className="btn btn-accent btn-md mt-2"
                            onClick={handleAddEvaluation}
                            title='Add evaluation'
                        >
                            Add Evaluation
                        </button> */}
                    </div>


                    <hr className="my-4 border-t border-gray-300 mt-5 mb-5" />
                    <div className="flex justify-center">
                        <button
                            className="btn btn-accent btn-md"
                            onClick={handleSubmitManual}
                            disabled={!evaluations.length}
                            title='Submit evaluations'
                        >
                            Submit Manually
                        </button>
                    </div>

                </div>

            </dialog >
        </div >
    );
};

export default SubmitPage;
