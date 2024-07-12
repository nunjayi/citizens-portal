import React, { useState,useContext } from "react";
import '../styles/project.css'
import { UserContext } from './context/userContext';


function Project(){


   const {currentUser,logout,project} = useContext(UserContext)
   const [description,setDescription] = useState()
   const [amount,setAmount] = useState()
   const [date, setDate] = useState()
   const [status,setStatus] = useState()
   const [signed,setSigned] = useState()
   const [ministry,setMinistry] = useState()

   
   const handleSubmit =(e)=>{
      e.preventDefault()   
      setDate(new Date)
      setStatus('incomplete')
      setSigned(currentUser.name)

      project(description,amount,date,status,signed,ministry)
   }



    return(
       <div>
         <header>
            <h1>Create a new Project !</h1>
            <p>Allocated budget: <span>1000000</span></p>
         </header>
         <div>
            <form className="login" onSubmit={handleSubmit}>
                    <h2>New Project</h2>
                    <input type='number' placeholder="ministry id" minLength={1} max={3}  required value={ministry || ""} onChange={(e)=> setMinistry(e.target.value)}/> 
                    <p>Enter project details</p>
                    <input type="textarea" placeholder="describe the project" required value={description || ""} onChange={(e)=> setDescription(e.target.value)} />
                    <p>Budget</p>
                    <input type='number' placeholder="amount you wish to spend" required value={amount || ""} onChange={(e)=> setAmount(e.target.value)} />
                    <input type="submit" value="Add" />
            </form>   
         </div>

       </div>
    )
}

export default Project