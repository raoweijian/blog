'use strict';

function sleep(ms){
    return new Promise(resolve => setTimeout(resolve, ms));
}

function imgReader(item){
    let blob = item.getAsFile();
    let reader = new FileReader();
    let ret = "";
    reader.onload = function(e){
    };
    reader.readAsDataURL(blob);
    return reader;
}
