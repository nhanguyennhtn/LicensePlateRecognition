import Headers from "../components/Header"
import '../assets/scss/HomePage.scss'

export default function HomePage() {
    return (
        <div className="home-wrapper card container-xxl">
            <div className=" bg-white ">
                <Headers />
                <div className="container-xxl">
                    <div className="row justify-content-center">
                        <div className="col-xl-6 col-sm-8">
                            <div className="card border-0">
                                <div className="card-block ">
                                    <h2 className=" card-header border-0 text-center mb-3 bg-white ">Đăng nhập!</h2>
                                    <div className="card-body border-0 pt-0">
                                        <div className="row justify-content-center">
                                            <form className='mt-3 form-login'>
                                                <div class="form-group p-1 mb-3">
                                                    <input type="text" name="username" className="form-control p-2" placeholder="Username" />
                                                </div>
                                                <div class="form-group p-1">
                                                    <input type="password" name="username" className="form-control p-2" placeholder="Password" />
                                                </div>
                                                <div className="row mt-3 px-3">
                                                    <button type="submit" className="btn btn-primary btn-block mt-3"> Login</button>
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

        </div>
    )
}