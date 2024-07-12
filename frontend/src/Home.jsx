import { useState } from 'react'
import { Link,useNavigate } from 'react-router-dom'

import './home.css'

function Home() {
  const [count, setCount] = useState(0)
  const nav = useNavigate()

  return (
    <>
    <div class="hero">
      <navbar>
       <div></div>
        <div>
          <button type="button" onClick={()=>{nav('/civillogin')}}>civil</button>
          <button type="button"  onClick={()=>{nav('/login')}}>Login</button>
          <button type="button"  onClick={()=>{nav('/signup')}}>Sign Up</button>
        </div>
      </navbar>
      <div class="content">
        <h3>Welcome to Citizen services</h3>
        <h1>Tujijenge kila siku <br/> tujiendeleshe</h1>
        
      </div>
    </div>


  </>
  )
}

export default Home
