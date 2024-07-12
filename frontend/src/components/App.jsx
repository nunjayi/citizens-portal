import React from "react"; 


import { BrowserRouter, Routes, Route } from "react-router-dom";


import Home from '../Home'
import Login from "./login";
import Error from "./error"
import Project from "./project";
import Reports from "./reports";
import Signup from "./signup";
import Tenders from "./tenders";
import Dashboard from "./dashboard";
import CivilDashboard from "./civilDashboard";
import CivilLogin from "./civillogin";
import { UserProvider } from "./context/userContext";
import { CivilProvider } from "./context/civilContext";
import { ProjectProvider } from "./context/projectContext";





function App() {

    return (     
      <BrowserRouter>
      <ProjectProvider />
      <CivilProvider>
       <UserProvider>
        <Routes>
          
            <Route path='/' element={<Home />} />
            <Route path='/dashboard' element={<Dashboard />} />
            <Route path='/signup' element={<Signup />} />
            <Route path='/login' element={<Login />} />
            <Route path='/project' element={<Project />} />
            <Route path='/tenders' element={<Tenders />} />
            <Route path='/reports' element={<Reports />} />
            <Route path = '/civicdash' element ={<CivilDashboard />} />
            <Route path="/civillogin" element = {<CivilLogin />} />

  
            <Route path="*" element={<Error />} />
          
        </Routes>
      </UserProvider>
      </CivilProvider>
      <ProjectProvider />
      </BrowserRouter>
    )
  }
  
export default App
