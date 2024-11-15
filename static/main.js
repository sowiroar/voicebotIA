document.addEventListener("DOMContentLoaded", function() { 
        
    document.getElementById("report").classList.add("oculto");
    document.getElementById("wave").classList.remove("oculto");

    recorder("/audio", response => {
        document.getElementById("record").style.display="";
        document.getElementById("stop").style.display="none";
        
        if (!response || response == null) {
            console.log("No response");
            return;
        }
        console.log("El texto fue: " + response.text)
        document.getElementById("text").innerHTML = response.text;
        if (typeof response.file !== "undefined") {
            // Reproducir el audio que regreso Python (si existe)
            audioFile = response.file;
            let audio = new Audio();
            audio.setAttribute("src", "static/" + audioFile + "?t=" + new Date().getTime());
            audio.play();

            document.getElementById("report").classList.remove("oculto");
            document.getElementById("wave").classList.add("oculto");
        }
    });
});