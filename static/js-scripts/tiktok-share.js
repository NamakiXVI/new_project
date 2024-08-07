function share_tiktok(id) {
    console.log(id);
    var share_link = String(document.getElementById(id).value);
    console.log(share_link);

    if(share_link)
    {
        var tempInput = document.createElement("input");
        tempInput.setAttribute("value", share_link);
        document.body.appendChild(tempInput);

        tempInput.select();
        tempInput.setSelectionRange(0, 99999); // For mobile devices
        navigator.clipboard.writeText(tempInput.value);
        window.open(share_link);

        document.body.removeChild(tempInput);
    }
}

function reload_videos(){
    location.reload();
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0;
}

function link_to(){
    link = "https://namakixvi.github.io/Projectlibrary-by-namaki/";
    current_window = currentWindow.location.href;
    window.open(link);
    current_window.close();
    history.back();
}