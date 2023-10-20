export interface Result {
    faculty: string;
    course: string;
    lecturer: string;
    semesters: string[];
    topics: {
        [topic: string]: number[];
    };
};