import { Link } from "react-router-dom";
import '../assets/scss/register.scss'
import React, { useState } from 'react';
import axios from 'axios';


export default function Login() {
    const [form, setForm] = useState({ TenDangNhap_TK: '', MatKhau_TK: '' })
    const [error, setError] = useState('')

    const handleChange = (e) => {
        const { name, value } = e.target;
        setForm({ ...form, [name]: value });
    }

    const handleSubmit = (e) => {
        e.preventDefault()
        axios.post('http://localhost:5000/api/login', form)
            .then(response => {
                const token = response.data.token
                sessionStorage.setItem('token', token)
                if (response.data.PhanQuyen_TK === 'admin') {
                    window.location.href = '/admin'
                }
                else if (response.data.PhanQuyen_TK === 'nhanvien') {
                    window.location.href = '/'
                }
            })
            .catch(error => {
                if (error.response && error.response.data && error.response.data.error) {
                    setError(error.response.data.error);
                } else {
                    setError('Thông tin chưa chính xác');
                }
                console.error('Đã có lỗi khi truy cập!', error);
            });
    }

    return (
        <div className="wrapper">
            <div className="container main">
                <div className="row " style={{ width: 500 + 'px' }}>
                    <div className="card">
                        <div className="">
                            <div className="card-block align-items-center">
                                <h2 className=" card-header border-0 text-center mb-3 bg-white ">Đăng nhập!</h2>

                                <div className="card-body border-0 pt-0">
                                    <div className="row justify-content-center">
                                        <form className='mt-3 form-login' onSubmit={handleSubmit}>
                                            <div class="form-group p-1 mb-3">
                                                <input className='p-2 w-100' type="text" name="TenDangNhap_TK" value={form.TenDangNhap_TK} onChange={handleChange} placeholder="Tên đăng nhập" required />
                                            </div>
                                            <div class="form-group p-1">
                                                <input className='p-2 w-100 mb-1' type="password" name="MatKhau_TK" value={form.MatKhau_TK} onChange={handleChange} placeholder="Mật khẩu" required />
                                            </div>
                                            <div class="form-group pb-0 mt-1">
                                                <span className="ps-2">Bạn chưa có tài khoản? <Link to={'/register'}>Đăng ký</Link></span>
                                            </div>
                                            <div className="row mt-1 px-3">
                                                <button type="submit" className="btn btn-primary btn-block mt-3"> Login</button>
                                            </div>
                                            <div class="form-group pb-0 mt-1">
                                                <div className='ps-2 text-center'> {error && <p style={{ color: 'red' }}>{error}</p>}</div>
                                            </div>
                                        </form>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    )
}