import { Link } from 'react-router-dom'

export default function ContentMenu() {
    return (
        <nav id="sidebarMenu" class="col-md-3 col-lg-2 d-md-block bg-light sidebar collapse">
            <div class="position-sticky pt-3">
                <ul class="nav flex-column">
                    <li class="nav-item">
                        <Link class="nav-link" aria-current="page" to="/admin">
                            <i class="bi bi-houses "></i> Trang chủ
                        </Link>
                    </li>
                    <li class="nav-item">
                        <Link class="nav-link" to="/admin/room">
                            <i class="bi bi-stack"></i> Bãi xe
                        </Link>
                    </li>
                    <li class="nav-item p-auto ">
                        <div class="btn-group ">
                            <button class="btn nav-link " type="button" data-bs-toggle="dropdown" aria-expanded="false">
                                <i class="bi bi-card-text"></i> Thống kê <i class="bi bi-chevron-right ms-auto"></i>
                            </button>
                            <ul class="dropdown-menu w-100 ms-3">
                                <li><Link className='nav-item text-dark text-decoration-none' to={'/admin/info-car-out'}>Thông tin xe ra</Link></li>
                                <hr class="sidebar-divider"/>
                                
                                <li><Link className='nav-item text-dark text-decoration-none' to={'/admin/info-car-in'}>Thông tin xe vào</Link></li>
                            </ul>
                        </div>
                        {/* <button class="btn nav-link " type="button" data-bs-toggle="dropdown" aria-expanded="false">
                            <i class="bi bi-card-text"></i> Thống kê <i class="bi bi-chevron-right ms-auto"></i>
                        </button>
                        <ul class="dropdown-menu">
                            <li><Link>Thông tin nhân viên</Link></li>
                        </ul> */}
                        {/* <button class="nav-link " to="/admin/statistic">
                            <i class="bi bi-card-text"></i> Thống kê
                        </button> */}
                    </li>
                    <li class="nav-item">
                        <Link class="nav-link" to="/admin/customers">
                            <i class="bi bi-people-fill"></i> Khách hàng
                        </Link>
                    </li>
                    <li class="nav-item">
                        <Link class="nav-link" to="/admin/contact">
                            <i class="bi bi-person-lines-fill"></i> Thông tin xe
                        </Link>
                    </li>

                    {/* <li class="nav-item">
                        <Link class="nav-link" to="/admin/bill">
                            <i class="bi bi-receipt"></i> Hóa đơn
                        </Link>
                    </li> */}
                </ul>
                <h6 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-muted">
                    <span>Hoạt động</span>
                </h6>
                <ul class="nav flex-column mb-2">
                    <li class="nav-item">
                        <Link class="nav-link" to="/admin/response">
                            <i class="bi bi-reply-all-fill"></i> Xác nhận đăng ký xe
                        </Link>
                    </li>
                    {/* <li class="nav-item">
                        <Link class="nav-link" to="/admin/response-news">
                            <i class="bi bi-reply-all-fill"></i>Tin tức
                        </Link>
                    </li>
                    <li class="nav-item">
                        <Link class="nav-link" to="/admin/expense">
                            <i class="bi bi-droplet-fill"></i> Điện nước phòng
                        </Link>
                    </li> */}

                </ul>
            </div>
        </nav>
    )
}