import Headers from "../components/Header"
import '../assets/scss/HomePage.scss'
import Webcam from 'react-webcam';
import { useCallback, useEffect, useRef, useState } from "react";
import axios from "axios";
import WebcamComponent from "../components/WebcamComponent";

export   default function HomePage() {
    const [biensoND1, setBiensoND1] = useState('')
    const [biensoND2, setBiensoND2] = useState('')
    const [baixe, setBaixe] = useState('BX001')
    const [result, setResult] = useState([])

    const webcamRef = useRef(null);
    const [imageSrc, setImageSrc] = useState('')
    const [, setShowWebcam] = useState(true)

    useEffect(() => {
        fetchData()
    }, [biensoND1, biensoND2])

    const fetchData = () => {
        axios.get(`http://localhost:5000/api/search_by_plate`, {
            params: { bienso_ND: biensoND1 || biensoND2 },
        })
            .then(response => {
                setResult(response.data);
            })
            .catch(error => {
                console.error("There was an error fetching the data!", error);
                setResult(null)
            })
    }

    const capture = useCallback(() => {
        const imageSrc = webcamRef.current.getScreenshot();
        setImageSrc(imageSrc)
        setShowWebcam(false)
    }, [webcamRef])

    const handleSubmit = (event) => {
        event.preventDefault()
        const newxeVao = {
            bienso_XV: ('XV_' + biensoND1) || ('XV_' + biensoND2),
            anh_XV: imageSrc,
            thoigian_XV: result.thoigian,
            MSSV: result.MSSV,
            ma_CC: result.congchuc,
            ma_BX: baixe,
        }
        axios.post('http://localhost:5000/api/xevao/create', newxeVao)
            .then(response => {
                console.log('Xevao added successfully:', response.data);
                setImageSrc('')
                setBiensoND1('')
                setBiensoND2('')
                setResult('')
                setShowWebcam(true)
            })
            .catch(error => {
                console.error('Error adding Xevao:', error);
            });
        fetchData()
    }
    // console.log(result, 'jj');   

    

    return (
        <div>
            <div className="home-wrapper card container-xxl">
                <div className=" bg-white ">
                    <Headers />
                    <div className="row container-fluid">
                        <div className="d-flex justify-content-evenly gap-2">
                            <div className="card  algin col-xxl-4">
                                <div className="row w-100">
                                    <label className="text-center text-uppercase fw-bold">Cổng vào</label>
                                    <div className="card algin col-xxl-12 ms-2">
                                        <label className="text-center text-uppercase fw-bold">Thông tin xe vào</label>
                                        <div className="card">
                                            {/* <button type="button" onClick={capture}>Chụp ảnh</button> */}
                                            <WebcamComponent/>
                                        </div>
                                        <div className="d-inline-flex gap-3 ms-1">
                                            <div className="card col " >
                                                {imageSrc ? (
                                                    <div>
                                                        <img src={imageSrc} alt="Captured" className="w-100" />
                                                    </div>
                                                )
                                                    :
                                                    <img src="" alt="anh_xevao" style={{ width: 9 + "em", height: 8 + "em" }} />
                                                }

                                            </div>
                                            <div className="card col">
                                                <img src={result?.anh_xe} alt="image_thanhvien" style={{ width: 9 + "em", height: "auto" }} />
                                            </div>
                                        </div>
                                        <div className="d-flex flex-column ms-2 pt-2">
                                            <div className="pb-2 pe-2">
                                                <label className="col-3">Biển số</label>
                                                <input type="text" className=" col-4" value={biensoND1} onChange={(e) => setBiensoND1(e.target.value)} />
                                                <button className="submit ms-2" type='submit' onClick={handleSubmit}>xác nhận</button>
                                            </div>
                                        </div>
                                        <div className="d-flex flex-column ms-2">
                                            <div className="py-2 pe-2 ">
                                                <label className="col-3">Thông tin </label>
                                                <input type="text" className=" col-4 " value={result?.chucvu} placeholder={result?.chucvu} readOnly />
                                                <select className="ms-2" value={baixe} onChange={(e) => setBaixe(e.target.value)}>
                                                    <option value='BX001' >Bãi xe 1</option>
                                                    <option value='BX002'>Bãi xe 2</option>
                                                </select>
                                            </div>
                                            <div className="pb-2 pe-2">
                                                <label className="col-3">Biển số</label>
                                                <input type="text" className=" col-9" value={biensoND1} readOnly />
                                            </div>
                                            <div className="pb-2 pe-2">
                                                <label className="col-3">Số thẻ</label>
                                                <input type="text" className=" col-9" value={result?.MSSV || result?.congchuc || ''} readOnly />
                                            </div>
                                            <div className="pb-2 pe-2">
                                                <label className="col-3">Thời gian</label>
                                                <input type="text" className=" col-9" value={result?.thoigian} readOnly />
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div className="card algin col-xxl-8">
                                <div className="row w-100 ms-1 p-1">
                                    <label className="text-uppercase text-center fw-bold">Cổng ra</label>
                                    <div className="card  algin col-xxl-6">
                                        <label className="text-center text-uppercase fw-bold">Thông tin xe vào</label>
                                        <div className="card">
                                            {/* <Webcam
                                        audio={false}
                                        ref={webcamRef}
                                        screenshotFormat="image/jpeg"
                                        videoConstraints={{
                                            facingMode: "environment"
                                        }}
                                        style={{ padding: 4 + 'px'}}
                                    /> */}
                                            <button type="button" onClick={capture}>Chụp ảnh</button>
                                        </div>
                                        <div className="d-inline-flex gap-3 ms-1">
                                            <div className="card col " >
                                                {imageSrc ? (
                                                    <div>
                                                        <img src={'imageSrc'} alt="Captured" className="w-100" />
                                                    </div>
                                                )
                                                    :
                                                    <img src="" alt="anh_xera" style={{ width: 9 + "em", height: 8 + "em" }} />
                                                }

                                            </div>
                                            <div className="card col">
                                                <img src={result?.anh_xe} alt="image_thanhvien" style={{ width: 9 + "em", height: "auto" }} />
                                            </div>
                                        </div>
                                        <div className="d-flex flex-column ms-2 pt-2">
                                            <div className="pb-2 pe-2">
                                                <label className="col-3">Biển số</label>
                                                <input type="text" className=" col-4" value={''} onChange={(e) => setBiensoND1(e.target.value)} />
                                                <button className="submit ms-2" type='submit' >xác nhận</button>
                                            </div>
                                        </div>

                                        <div className="d-flex flex-column ms-2">
                                            <div className="py-2 pe-2">
                                                <label className="col-3">Thông tin Xe</label>
                                                <input type="text" className=" col-4 " value={''} readOnly />
                                            </div>
                                            <div className="pb-2 pe-2">
                                                <label className="col-3">Biển số</label>
                                                <input type="text" className=" col-9" value={''} readOnly />
                                            </div>
                                            <div className="pb-2 pe-2">
                                                <label className="col-3">Số thẻ</label>
                                                <input type="text" className=" col-9" value={''} readOnly />
                                            </div>
                                            <div className="pb-2 pe-2">
                                                <label className="col-3">Thời gian</label>
                                                <input type="text" className=" col-9" value={''} readOnly />
                                            </div>
                                        </div>


                                    </div>
                                    <div className="card  algin col-xxl-6">
                                        <label className="text-center text-uppercase fw-bold">Thông tin xe ra</label>
                                        <div className="card">
                                            {/* <Webcam
                                        audio={false}
                                        ref={webcamRef}
                                        screenshotFormat="image/jpeg"
                                        videoConstraints={{
                                            facingMode: "environment"
                                        }}
                                        style={{ padding: 4 + 'px'}}
                                    /> */}
                                            <button type="button" onClick={capture}>Chụp ảnh</button>
                                        </div>
                                        <div className="d-inline-flex gap-3 ms-1">
                                            <div className="card col " >
                                                {imageSrc ? (
                                                    <div>
                                                        <img src={'imageSrc'} alt="Captured" className="w-100" />
                                                    </div>
                                                )
                                                    :
                                                    <img src="" alt="anh_xevao" style={{ width: 9 + "em", height: 8 + "em" }} />
                                                }

                                            </div>
                                            <div className="card col">
                                                <img src={result?.anh_xe} alt="image_thanhvien" style={{ width: 9 + "em", height: "auto" }} />
                                            </div>
                                        </div>
                                        <div className="d-flex flex-column ms-2 pt-2">
                                            <div className="pb-2 pe-2">
                                                <label className="col-3">Biển số</label>
                                                <input type="text" className=" col-4" value={biensoND2} onChange={(e) => setBiensoND2(e.target.value)} />
                                                <button className="submit ms-2" type='submit' >xác nhận</button>
                                            </div>
                                        </div>

                                        <div className="d-flex flex-column ms-2">
                                            <div className="py-2 pe-2">
                                                <label className="col-3">Thông tin Xe</label>
                                                <input type="text" className=" col-4 " value={''} readOnly />
                                            </div>
                                            <div className="pb-2 pe-2">
                                                <label className="col-3">Biển số</label>
                                                <input type="text" className=" col-9" value={''} readOnly />
                                            </div>
                                            <div className="pb-2 pe-2">
                                                <label className="col-3">Số thẻ</label>
                                                <input type="text" className=" col-9" value={''} />
                                            </div>
                                            <div className="pb-2 pe-2">
                                                <label className="col-3">Thời gian</label>
                                                <input type="text" className=" col-9" value={''} />
                                            </div>
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