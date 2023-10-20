import React, { useState } from 'react';
import Plot from 'react-plotly.js';
import { Result } from '../types/results';
import * as d3 from 'd3';

import SearchBar from '../components/GeneralSearchBar';
// import SearchBar from '../components/SearchBar';


const Dashboard: React.FC = () => {
    const CONFIG = { displayModeBar: false, scrollZoom: true };
    const colorScale = d3.scaleOrdinal(d3.schemeTableau10);

    const [fetchedData, setFetchedData] = useState<Result>({} as Result);

    const manipulateDataLineChart = (input_data: Result) => {
        const dat_for_dasboard = []
        const topics = Object.keys(input_data.topics)
        for (let i = 0; i < topics.length; i++) {
            const topic = topics[i]

            const data = {
                x: input_data.semesters,
                y: input_data.topics[topic],
                type: 'scatter',
                mode: 'lines+markers',
                marker: { color: colorScale(topic) },
                name: topic,
                hovertemplate: `${input_data.course}<br>Semester: %{x}<br>Topic:${topic}<br>Topic Distribution: %{y}<extra></extra>`
            }
            dat_for_dasboard.push(data)
        }
        return dat_for_dasboard
    }

    const manipulateDataAreaChart = (input_data: any) => {
        const dat_for_dasboard = []
        const topics = Object.keys(input_data.topics)
        for (let i = 0; i < topics.length; i++) {
            const topic = topics[i]
            const data = {
                x: input_data.semesters,
                y: input_data.topics[topic],
                type: 'scatter',
                mode: 'lines',
                fill: 'tozeroy',
                marker: { color: colorScale(topic) },
                name: topic,
                hovertemplate: `${input_data.course}<br>Semester: %{x}<br>Topic:${topic}<br>Topic Distribution: %{y}<extra></extra>`
            }
            dat_for_dasboard.push(data)
        }
        return dat_for_dasboard
    }


    const manipulateDataStackedBarChart = (input_data: any) => {
        const dat_for_dasboard = []
        const topics = Object.keys(input_data.topics)
        for (let i = 0; i < topics.length; i++) {
            const topic = topics[i]
            const data = {
                x: input_data.semesters,
                y: input_data.topics[topic],
                type: 'bar',
                marker: { color: colorScale(topic) },
                name: topic,
                hovertemplate: `${input_data.course}<br>Semester: %{x}<br>Topic:${topic}<br>Topic Distribution: %{y}<extra></extra>`

            }
            dat_for_dasboard.push(data)
        }
        return dat_for_dasboard
    }

    const createLayout = (input_data: any) => {
        return {
            title: 'Topic distribution over time for ' + input_data.course + ' course',
            titlefont: {
                color: 'white',
            },
            xaxis: {
                type: 'date',
                title: 'Date',
                tickformat: '%B - %Y',
                tickvals: input_data.semesters,
                color: 'grey',

            },
            yaxis: {
                title: 'Topic Distribution',
                tickformat: ',.0%',
                range: [0, 1.1],
                color: 'grey',

            },
            legend: {
                orientation: 'h',
                yanchor: 'bottom',
                y: 1.02,
                xanchor: 'right',
                x: 1,
                font: {
                    color: 'white',
                }
            },
            plot_bgcolor: 'transparent',
            paper_bgcolor: 'transparent',
            barmode: 'stack',

        };
    }



    const handleDataFetched = (data: Result) => {
        setFetchedData(data);
    };

    return (
        <div className="container mx-auto px-4">
            <div className="flex flex-wrap mx-auto max-w-screen justify-center pt-5 w-2/3">
                <SearchBar responseType="result" onDataFetched={handleDataFetched} /> {/*solve this error, even tho all works*/}
            </div>
            <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-2">
                {Object.keys(fetchedData).length === 0 ? (
                    <p className="col-span-2">No data available.</p>
                ) : (
                    <>
                        <div>
                            <Plot data={manipulateDataLineChart(fetchedData)} layout={createLayout(fetchedData)} config={CONFIG} />
                        </div>
                        <div>
                            <Plot data={manipulateDataStackedBarChart(fetchedData)} layout={createLayout(fetchedData)} config={CONFIG} />
                        </div>
                        <div>
                            <Plot data={manipulateDataAreaChart(fetchedData)} layout={createLayout(fetchedData)} config={CONFIG} />
                        </div>
                    </>
                )}
            </div>
        </div>
    );
};

export default Dashboard;