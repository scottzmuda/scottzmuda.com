function getUTCOffset(){
    formElement = document.getElementById("utc_offset_minutes");

    if( !formElement ){
        return;
    }

    localDate = new Date();
    offset = localDate.getTimezoneOffset();

    formElement.value = offset;
}

async function onPageLoad(){
    getUTCOffset();
}

onPageLoad();