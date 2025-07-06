import React from "react";

function Input({placeHolder, widthInput, type, value, onChange}){
    const width = widthInput || "w-full";
    return(
        <>
            <input 
            type={type} 
            placeholder={placeHolder} 
            value={value}
            onChange={onChange}
            className={`${width} bg-white h-10 border-2 rounded-lg text-center hover:bg-gray-200 transition duration-200 `}/>
        </>
    );  
}



export default Input;

