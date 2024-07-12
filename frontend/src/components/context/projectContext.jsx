import { createContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export const ProjectContext = createContext();


export const ProjectProvider = ({children}) => {
    const nav = useNavigate();

   



        
// Register User
const addProject = (description,amount,date,status,signed,ministry_id) => {
    fetch('http://localhost:8080/newProject', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            description:description,
            amount:amount,
            date:date,
            status:status,
            signed : signed,
            ministry_id:ministry_id
           
        })
    })
    .then(res => res.json())
    .then(res => {
        console.log(res);
    if(res.success)
        {
            nav('/login')
        alert(res.success)
    }
    else if(res.error){
        alert(res.error)
    }
    else{
        alert("Something went wrong")
    }
        
    })

}



  const contextData ={

    addProject
  }


  return (
    <ProjectContext.Provider value={contextData}>
        {children}
    </ProjectContext.Provider >
  )


}