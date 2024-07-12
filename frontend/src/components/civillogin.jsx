import React, { useContext, useState }  from 'react'
import { Link } from 'react-router-dom'
import { CivilContext } from './context/civilContext'

import '../styles/login.css'



function CivilLogin(){
   //submit a new user
   const {login} = useContext(CivilContext)
   const [email, setEmail] = useState()
   const [password, setPassword] = useState()


   console.log(email, password);
   
   function handleSubmit(e){
       e.preventDefault()

       login(email, password)

   }



    return(
        <>
            <form className="login" onSubmit={handleSubmit}>
                <h2>Welcome, User!</h2>
                <p>Please log in</p>
                
                <input type="email" placeholder="email address" required  value={email || ""} onChange={(e)=> setEmail(e.target.value)}/>
                <input type="password" placeholder="Password" required value={password || ""} onChange={(e)=> setPassword(e.target.value)}/>
                <input type="submit" value="Log In" />
                <div className="links">
                    <a href="#">Forgot password</a>
                    
                </div>
            </form>   
           

        </>
    )
}
export default CivilLogin