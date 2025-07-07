import HandleApiCalls from "../auth/Api";
import Input from "../miniComponents/Input";
import Button from "../miniComponents/Button";
import Title from "../miniComponents/Title";
import React, { useState } from "react";

const api = new HandleApiCalls();
function Loginform(){
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const event  = async () => {
        await api.Login(email, password).then((res) =>{
            const token = res.access;
            localStorage.setItem("token", token);
            window.location.reload();
        }).catch((e)=> {
            console.log("Error:", e);
        })

    }
    return(
        <>

                <Title fileName={"BmoSayingHi.png"} text={"Sign In"}/>


                <div className="w-[375px] h-[300px] flex flex-col items-center justify-center gap-[15px] ">

                    
                    <Input 
                    widthInput={"w-[355px]"} 
                    placeHolder={"Email:"}
                    type={"email"}
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}/>


                    <Input 
                    widthInput={"w-[355px]"} 
                    placeHolder={"Password:"} 
                    type={"password"}
                    value={password}
                    onChange={(e) => setPassword(e.target.value) }/>


                    <h1 className=" underline text-white sm:text-black">
                        Forgot Password?
                    </h1>

                </div>
               <Button 
               marginBottom={"mb-5"}
               text={"Login"} 
               event={event} 
               widthButton={"w-[190px]"}
               heightButton={"h-[48px]"}/>

            </>
    );
}




export default Loginform;                                      