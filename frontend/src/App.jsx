import SignPage from './components/pages/signPage'
import { useEffect } from "react";
import HandleApiCalls from './components/auth/Api';

const api = new HandleApiCalls();
function App() {

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const uid = params.get("uid");
    const token = params.get("token");

    if (uid && token) {
      // Call backend to verify email
      api.VerifyEmail(uid, token)
        .then((res) => {
          console.log("Email verified:", res.data);
          // maybe redirect or show success message
        })
        .catch((err) => {
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
