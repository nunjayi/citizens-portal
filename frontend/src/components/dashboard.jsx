import React ,{useContext} from 'react'
import { UserContext } from './context/userContext';
import {Link,Outlet,useNavigate} from 'react-router-dom'
import {ToastContainer} from 'react-toastify'


import 'bootstrap-icons/font/bootstrap-icons.css';
import '../styles/dashboard.css'
function Dashboard(){
    const nav =useNavigate()
    const {currentUser,logout} = useContext(UserContext)

    return(
       <>
            <div className="dashboard">
               <nav id='navbar'>
                    <div id='navigation'>
                        <div className='logo'> <span>{currentUser.name[0]} </span> </div>
                        <div className="navitem" onClick={()=>{nav('/project')}}><i class="bi bi-clipboard-data-fill"></i>  Projects</div>
                        <div className="navitem" onClick={()=>{nav('/tenders')}}><i class="bi bi-cart3"></i>  Tenders</div>
                        <div className="navitem" onClick={()=>{nav('/reports')}}> <i class="bi bi-file-earmark-bar-graph-fill"></i> Reports</div>
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
                       <div className='table'>


                    </div>
                    <br /><br /><br />

                    <div className='table'>
                        
                            
                            <div className="column">
                                <div className="row">Description</div>
                                <div className="row">Amount</div>
                                <div className="row">Status</div>
                                <div className="row">Signed</div>


                            </div>
                            <hr />
                            <div className="column">
                                <div className="row">repair limuru highway</div>
                                <div className="row">1000000</div>
                                <div className="row">in progress</div>
                                <div className="row">Ryan Garcia</div>


                            </div>
                            <hr />
                            <div className="column">
                                <div className="row">build kapsaret highway</div>
                                <div className="row">1000000</div>
                                <div className="row"> in progress</div>
                                <div className="row">Ryan Garcia</div>


                            </div>
                            <hr />

                   </div>

                  
                      
                       </div>
                    </div>


               </main>


            </div>
       </>
    )
}

export default Dashboard

