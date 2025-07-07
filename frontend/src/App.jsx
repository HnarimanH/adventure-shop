import SignPage from './components/pages/signPage'
import { use, useEffect, useState } from "react";
import HandleApiCalls from './components/auth/Api';
import Dashboard from './components/pages/dashboard';

const api = new HandleApiCalls();
function App() {

  const [isLogedIn, setIsLogedIn] = useState(() => {
  if (localStorage.getItem("token")){ return true; }
  return false;
});
  
  useEffect(() => {
  const interval = setInterval(() => {
    api.deleteInactiveUser()
  }, 2 * 60 * 1000);
  return () => clearInterval(interval); 
}, []);



  
  useEffect(() => {
  const verifyAndLogin = async () => {
    const params = new URLSearchParams(window.location.search);
    const uid = params.get("uid");
    const token = params.get("token");

    if (uid && token) {
      try {
        const res = await api.VerifyEmail(uid, token);
        console.log("Email verified", res);
        
        setIsLogedIn(true);
      } catch (err) {
        console.error(
          "Verification or login failed:",
          err.response?.data || err.message
        );
      }
    }
  };

  verifyAndLogin();
}, []);
  return (
    <>
      <div className='w-screen h-screen flex justify-center items-center'>
          
          {isLogedIn ? <Dashboard/> : <SignPage/>}
      </div>
    </>
  )
}

export default App
