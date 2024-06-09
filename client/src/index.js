import React, { useState } from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import './index.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import '@fortawesome/fontawesome-free/css/all.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';

import Login from './auth/Login.js';
import Register from './auth/Register.js';
import HomePage from './page/index.js';
// import HomePage1 from './page/homepage.js';
import HomePageAdmin from './page/admin/adminHomePage.js';
import Customers from './page/admin/Customers.js';
import Xevao from './page/admin/xevao/index.js';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(!!sessionStorage.getItem('token'));
  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  return (
    <BrowserRouter>
      <Routes>
        <Route path='/login' element={<Login />} />
        <Route path='/register' element={<Register />} />
        <Route path='/admin' element={isLoggedIn ? <HomePageAdmin /> : <Login onLogin={handleLogin} />} />
        <Route path='/admin/customers' element={isLoggedIn ? <Customers /> : <Login onLogin={handleLogin} />} />
        <Route path='/admin/info-car-in' element={isLoggedIn ? <Xevao /> : <Login onLogin={handleLogin} />} />

        {/* <Route path="/" element={isLoggedIn ? <HomePage1 /> : <Login onLogin={handleLogin} />} /> */}
        <Route path="/" element={isLoggedIn ? <HomePage /> : <Login onLogin={handleLogin} />} />
      </Routes>
    </BrowserRouter>
  );
}
const root = ReactDOM.createRoot(document.getElementById('root'))
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);
