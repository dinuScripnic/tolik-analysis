import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/NavBar';
import Home from './pages/WelcomePage';
import SubmitPage from './pages/SubmitPage';
import SearchPage from './pages/SearchPage';
import Dashboard from './pages/Dasboardpage';
import 'tailwindcss/tailwind.css';


ReactDOM.render(
  <Router>
    <Navbar />
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/upload_evaluations" element={<SubmitPage />} />
      <Route path="/search_evaluations" element={<SearchPage />} />
      <Route path="/dashboard" element={<Dashboard />} />
    </Routes>
  </Router>,
  document.getElementById('root')
);
