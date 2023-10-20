import React from 'react';

const Home: React.FC = () => {
    return (
        <div className=" text-white min-h-screen flex flex-col items-center justify-center">
            <h1 className="text-4xl font-bold text-center mb-4 text-blue-600">
                Welcome to Student Evaluation Hub
            </h1>
            <p className="text-lg text-center text-gray-300 mb-8">
                Hey there! We're here to make managing student evaluations a breeze. Whether you're exploring data or fine-tuning courses, we've got you covered.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div className="p-6 border rounded-lg shadow-md items-center justify-center">
                    <h2 className="text-2xl font-semibold mb-4 text-blue-600">
                        Take Control
                    </h2>
                    <p className="text-gray-300 mb-4">
                        Add, tweak, and organize student evaluations for different years, courses, and faculties like a pro.
                    </p>
                    <a href="/upload_evaluations" className="btn btn-primary">Add New Evaluations</a>
                </div>
                <div className="p-6 border rounded-lg shadow-md items-center justify-center">
                    <h2 className="text-2xl font-semibold mb-4 text-blue-600">
                        Discover Insights
                    </h2>
                    <p className="text-gray-300 mb-4">
                        Dive into your evaluation data, uncover hidden gems, and make informed decisions that matter.
                    </p>
                    <a href="/search_evaluations" className="btn btn-success">View Evaluations</a>
                </div>
                <div className="p-6 border rounded-lg shadow-md items-center justify-center">
                    <h2 className="text-2xl font-semibold mb-4 text-blue-600">
                        Dynamic Topic Modeling
                    </h2>
                    <p className="text-gray-300 mb-4">
                        Create, analyze, and visualize dynamic topic models from your data.
                    </p>
                    <a href="/dashboard" className="btn btn-info">Go to Dashboard</a>
                </div>
            </div>
        </div>
    );
};

export default Home;
