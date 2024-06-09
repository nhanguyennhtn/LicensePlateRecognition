// import { useState } from "react";
// import { useNavigate } from "react-router-dom"
import AdminHeader from './components/Header.js'
import ContentMenu from './components/ContentMenu.js'
import '../../assets/scss/dashboard.scss'

export default function AdminHomePage() {
    

    return (
        <div className="wrapper">
            <AdminHeader />
            <div class="container-fluid">
                <div class="row">
                    <ContentMenu />
                    <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
                        <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
                            <h1 class="h4 ms-4">Danh sách</h1>
                        </div>
                    </main>
                </div>
            </div>
        </div>
    )
}