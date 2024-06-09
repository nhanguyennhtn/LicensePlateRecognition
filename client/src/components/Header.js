import { useState } from 'react';
import '../assets/scss/Header.scss'
import {  Link, useNavigate } from 'react-router-dom';

export default function Header() {
    const navigate = useNavigate()
    const [, setIsLoggedIn] = useState(!!localStorage.getItem('token'));
    const handleLogout = () => {
        sessionStorage.removeItem('token');
        setIsLoggedIn(false);
        navigate('/login')
    };
    return (
        <div className="header-wrapper row ">
            <div className="px-2">
                <h2 className="h2">Logo</h2>
            </div>
            <nav class="navbar navbar-expand-lg navbar-light bg-light">
                <div class="container-fluid navbar-inner px-4 ">
                    <a class="navbar-brand text-white py-3 gap-5 justify-content-center " href="/">Trang chủ</a>
                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
                        <span class="navbar-toggler-icon"></span>
                    </button>
                    <div class="collapse navbar-collapse" id="navbarNavDropdown">
                        {/* <ul class="navbar-nav">
                            <li class="nav-item dropdown">
                                <a class="nav-link dropdown-toggle text-white" href="/" id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                    English
                                </a>
                                <ul class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
                                    <li><a class="dropdown-item" href="/">Enghlish(en)</a></li>
                                    <li><hr class="dropdown-divider" /></li>
                                    <li><a class="dropdown-item" href="/">Vietnamese(vi)</a></li>
                                </ul>
                            </li>
                        </ul> */}
                        <button className='btn ms-auto text-white border border-white me-2' onClick={() => handleLogout()}>Logout</button>
                        <Link to={'/profile'}><i class="bi bi-person-lines-fill text-white fs-4 ms-2 "></i></Link>
                    </div>
                </div>
            </nav>
        </div>
    )
}