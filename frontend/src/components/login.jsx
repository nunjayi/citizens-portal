import React, { useContext, useState }  from 'react'
import { Link } from 'react-router-dom'
import { UserContext } from './context/userContext'

import '../styles/login.css'



function Login(){
   //submit a new user
   const {login} = useContext(UserContext)
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
                <div class="links">
                    <a href="#">Forgot password</a>
                    <a href="signup">Register</a>
                </div>
            </form>   
           

        </>
    )
}
export default Login