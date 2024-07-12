import { createContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export const CivilContext = createContext();


export const CivilProvider = ({children}) => {
    const nav = useNavigate();

    const [authToken, setAuthtoken] = useState(()=> localStorage.getItem('token')? localStorage.getItem('token') : null);

   const [currentUser, setCurrentUser] = useState(null);



   
// Register User
const register = (name, email, password) => {
    fetch('http://localhost:8080/users', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: name,
            email: email,
            password: password 
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

// Login User
    const login =  (email, password) => {
        fetch('http://localhost:8080/civillogin', {
            method: 'POST',
            mode:'cors',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                password: password 
            })
        })
        .then(res => res.json())
        .then(res => {
            console.log(res);
        if(res.access_token)
            {
                setAuthtoken(res.access_token)
                localStorage.setItem('token', res.access_token)

                console.log(res);
                nav('/civicdash')
            alert("Login success")
        }
        else if(res.error){
            alert(res.error)
        }
        else{
            alert("Something went wrong")
        }
            
        })
        
    }

// Logout User
  function logout(){


        fetch('http://localhost:8080/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            }}
            )
            .then(res => res.json())
            .then(res => {
                console.log(res);
                if(res.success){
                    setAuthtoken(null)
                    localStorage.removeItem('token')
                    nav('/civillogin')
                }
            
                else{
                    alert("Something went wrong")
                }
            })
  }

  useEffect(() => {
    if(authToken){
        fetch('http://localhost:8080/current_user', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                "Authorization": `Bearer ${authToken}`
            }
        
        })
        .then(res => res.json())
        .then(res => {
            setCurrentUser(res)
        })

        
    }
    else{
        setCurrentUser(null)
    }
  }, [authToken])


  
        
// Register User
const project = (description,amount,date,status,signed,ministry_id) => {
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
            nav('/civicdash')
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
    currentUser,
    register,
    login,
    logout,
    project
  }


  return (
    <CivilContext.Provider value={contextData}>
        {children}
    </CivilContext.Provider >
  )


}