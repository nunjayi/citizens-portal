import React, { useContext, useState } from 'react'
import { Link } from 'react-router-dom'
import { UserContext } from './context/userContext'
import '../styles/signup.css'


function Register() 
{

  const {register} = useContext(UserContext)



  const [email, setEmail] = useState()
  const [password, setPassword] = useState()
  const [repeatPassword, setRepeatPassword] = useState()
  const [name, setName] = useState()

  console.log(email, password, repeatPassword, name);
  
  function handleSubmit(e){
    e.preventDefault()

    register(name, email, password)
  }


  return (
        
    <form className="signup" onSubmit={handleSubmit} >
        <h2>Create account!</h2>
        <p>Enter details</p>
        <input type="text" placeholder="User Name" required value={name || ""} onChange={(e)=> setName(e.target.value)} />
        <input type="email" placeholder="email address"  required value={email || ""} onChange={(e)=> setEmail(e.target.value)}  />
        <input type="password" placeholder="Password"  required value={password || ""} onChange={(e)=> setPassword(e.target.value)} />
        <input type="password" placeholder="repeat password"  required value={repeatPassword || ""} onChange={(e)=> setRepeatPassword(e.target.value)} />
        <input type="submit" value="Create Account" />

    </form>  
  )
}

export default Register