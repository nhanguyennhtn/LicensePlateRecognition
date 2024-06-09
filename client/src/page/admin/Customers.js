import AdminHeader from './components/Header.js'
import ContentMenu from './components/ContentMenu.js'
import { useEffect, useState } from 'react'
import axios from 'axios';

const InfoModal = ({ item, onClose }) => {
    return (
        <div className="modal" style={{ display: 'block', zIndex: 1000 }}>
            <div className="modal-dialog modal-dialog-centered">
                <div className="modal-content">
                    <div className="modal-header">
                        <h5 className="modal-title">Thông tin chi tiết</h5>
                        <button type="button" className="btn-close" onClick={onClose}></button>
                    </div>
                    <div className="modal-body">
                        <p><strong>Họ và tên:</strong> {item.ten}</p>
                        <p><strong>Số điện thoại:</strong> {item.sdt}</p>
                        <p><strong>Biển số xe:</strong> {item.bienso_xe}</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default function Customers() {
    const [data, setData] = useState([])

    useEffect(() => {
        fetchData()
    }, [])
    const fetchData = () => {
        axios.get('http://localhost:5000/api/admin/list-customers')
            .then(response => {
                setData(response.data);
            })
            .catch(error => {
                console.error("There was an error fetching the data!", error);
            });
    }
    const [showModal, setShowModal] = useState(false);
    const [selectedItem, setSelectedItem] = useState(null);

    const handleInfo = (item) => {
        setSelectedItem(item);
        setShowModal(true);
    };

    const handleCloseModal = () => {
        setShowModal(false);
    };
    console.log(data);
    return (
        <div className="wrapper">
            <AdminHeader />
            <div class="container-fluid">
                <div class="row">
                    <ContentMenu />
                    <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
                        <div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
                            <div className='row w-100'>
                                <div className='d-flex'>
                                    <select className='px-3'>
                                        <option defaultValue={'all'}>--Tất cả--</option>
                                        <option value={'canbo'}>Cán bộ</option>
                                        <option value={'sinhvien'}>Sinh viên</option>
                                    </select>
                                    <div className='ms-auto d-flex'>
                                        <input className='form-control ms-2' placeholder='Tìm kiếm' />
                                        <i className="bi bi-search align-self-center ms-2"></i>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className=''>
                            <table class="table table-bordered">
                                <thead>
                                    <tr>
                                        <th scope="col">#</th>
                                        <th scope="col">Họ và tên</th>
                                        <th scope="col">Số điện thoại</th>
                                        <th scope="col">Biển số xe</th>
                                        <th scope="col">Chỉnh sửa</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {data.map((item, index) => (
                                        <tr key={index}>
                                            <td>{++index}</td>
                                            <td>{item.ten}</td>
                                            <td>{item.sdt}</td>
                                            <td>{item.bienso_xe}</td>
                                            <td >
                                                <i class="bi bi-pencil-square text-primary ms-2 fs-5" ></i>
                                                <i class="bi bi-trash-fill text-danger ms-2 fs-5"></i>
                                                <i class="bi bi-info-circle text-warning ms-2 fs-5" onClick={() => handleInfo(item)}></i>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                            {showModal && <InfoModal item={selectedItem} onClose={handleCloseModal} />}
                        </div>
                    </main>

                </div>
            </div>
        </div>
    )
}