import axios from "axios"
import { useEffect, useState } from "react"

import AdminHeader from '../components/Header.js'
import ContentMenu from '../components/ContentMenu.js'
export default function Xevao() {
    const [xevao, setXevao] = useState([])

    useEffect(() => {
        fetchData()
    }, [])

    const fetchData = () => {
        axios.get('http://localhost:5000/api/xevao')
            .then((res) => {
                setXevao(res.data)
            })
            .catch(error => {
                console.error("There was an error fetching the data!", error)
            })
    }

console.log(xevao, '');
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
                    <div className='w-auto'>
                        <table class="table table-bordered">
                            <thead>
                                <tr>
                                    <th scope="col">#</th>
                                    <th scope="col">Biển số xe(vào)</th>
                                    <th scope="col">hình ảnh</th>
                                    <th scope="col">Thời gian xe vào </th>
                                    <th scope="col">Sinh viên</th>
                                    <th scope="col">Cán bộ</th>
                                    <th scope="col">Chỉnh sửa</th>
                                </tr>
                            </thead>
                            <tbody>
                                {xevao.length > 0 ? xevao.map((item, index) => (
                                    <tr key={index}>
                                        <td>{++index}</td>
                                        <td>{item.bienso_XV}</td>
                                        <td><img src={item.anh_XV} alt='image' style={{ width: 200 + 'px' }} /></td>
                                        <td>{item.thoigian_XV}</td>
                                        <td>{item.MSSV}</td>
                                        <td>{item.ma_CC}</td>
                                        <td >
                                            <i class="bi bi-pencil-square text-primary ms-2 fs-5" ></i>
                                            <i class="bi bi-trash-fill text-danger ms-2 fs-5"></i>
                                            <i class="bi bi-info-circle text-warning ms-2 fs-5" ></i>
                                        </td>
                                    </tr>
                                )):
                                <tr>không có dữ liệu</tr>
                                }
                            </tbody>
                        </table>
                        {/* {showModal && <InfoModal item={selectedItem} onClose={handleCloseModal} />} */}
                    </div>
                </main>
            </div>
        </div>
    </div>

)
}