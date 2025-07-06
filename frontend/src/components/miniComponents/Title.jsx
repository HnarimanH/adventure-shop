import React from "react";





function Title({text, fileName, }){
    return(
        <>
            <div style={{fontFamily:"cursive"}}
            className="h-[100px] w-[200px]  flex flex-row items-center justify-center">

                <img src={`./src/assets/${fileName}`} alt="image" className="h-full w-auto object-cover"/>



                <h1 className="text-2xl text-white text-shadow-lg/30 sm:text-black">
                   {text}
                </h1>


            </div>
        </>
    );
}




export default Title;