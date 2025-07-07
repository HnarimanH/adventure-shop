import SignPage from './components/pages/signPage'
import { use, useEffect, useState } from "react";
import HandleApiCalls from './components/auth/Api';


const api = new HandleApiCalls();
function App() {
  const [isLogedIn, setIsLogedIn] = useState(false)
  
  useEffect(() => {
  const interval = setInterval(() => {
    api.deleteInactiveUser()
  }, 2 * 0 * 1000);
  return () => clearInterval(interval); 
}, []);



  
  useEffect(async () => {
    
    const params = new URLSearchParams(window.location.search);
    const uid = params.get("uid");
    const token = params.get("token");

    if (uid && token) {
      // Call backend to verify email
      await api.VerifyEmail(uid, token).then((res) => {

          console.log("Email verified:");

          localStorage.setItem("token", token);
          
        }).catch((err) => {

          console.error("Email verification failed:", err.response?.data || err.message);

        });
    }
  }, []);

  return (
    <>
      <div className='w-screen h-screen flex justify-center items-center'>
          <SignPage/>
      </div>
    </>
  )
}

export default App
