import React from "react";


function Button({text, event, widthButton, heightButton, bgButton, marginBottom, hidden}){ 
    const hiddenInMobile = hidden || "flex"
    const mb = marginBottom || "";
    const bg = bgButton || "bg-white";
    const width = widthButton || "w-full";
    const height = heightButton || "h-full";
    return(
        <>
        <div onClick={event} className={`${width} ${height} ${bg} ${mb} hover:bg-gray-200 ${hiddenInMobile} items-center justify-center transition duration-200 border-2 rounded-lg cursor-pointer`}>
            <h1>
                {text}
            </h1>
        </div>
        </>
    );
}


export default Button; 