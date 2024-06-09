import React, { useState } from 'react'
import { Link, useNavigate } from "react-router-dom";

export default function Header() {
    const navigate = useNavigate()
    const [, setIsLoggedIn] = useState(!!localStorage.getItem('token'));
    const handleLogout = () => {
        sessionStorage.removeItem('token');
        setIsLoggedIn(false);
        navigate('/login')
    };
    
    return (
        <header class="navbar navbar-dark sticky-top bg-dark flex-md-nowrap p-2 shadow top-fixed">
            <Link class="navbar-brand col-md-3 col-lg-2 me-0 px-3 " to="/admin">Admin</Link>
            <div class="navbar-nav">
                <div class="dropdown ">
                    <button class="btn btn-secondary" onClick={handleLogout}>Đăng xuất</button>
                </div>
            </div>
        </header>
    )
}
