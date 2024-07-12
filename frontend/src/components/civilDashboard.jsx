import React ,{useContext} from 'react'
import { UserContext } from './context/userContext';
import {Link,Outlet} from 'react-router-dom'
import {ToastContainer} from 'react-toastify'
import { useNavigate } from "react-router-dom";


import 'bootstrap-icons/font/bootstrap-icons.css';
import '../styles/dashboard.css'

function CivilDashboard(){
    const nav= useNavigate()
    const {currentUser,logout} = useContext(UserContext)

    function newProject(){
        nav('/project')
    }

    return(
       <>
            <div className="dashboard">
               <nav id='navbar'>
                    <div id='navigation'>
                        <div className='logo'> <span>{currentUser.name[0]} </span> </div>
                        <div className="navitem" onClick={()=>{newProject()}}><i class="bi bi-plus-square-fill"></i>create Project</div>
                        <div className="navitem"><i class="bi bi-plus-square-fill"></i>  budget</div>
                        <div className="navitem"><i class="bi bi-hand-thumbs-up-fill"></i> tender</div>
                    </div>
                    <div id='account'>
                        <div className="navitem"> <i class="bi bi-person-circle"></i> Account</div>
                        <div className="navitem" onClick={()=>{logout()}}>
                            <i class="bi bi-box-arrow-left"></i> Logout
                        </div>
                    </div>
               </nav>
               <main>
                    <div className='header'>
                        <h2>Welcome {currentUser && currentUser.name}</h2>
                        <hr />
                       <div className='ministry'>

                       </div>
                    </div>


               </main>


            </div>
       </>
    )
}

export default CivilDashboard

