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

    // Manejar el clic del botón "Terminar Llamada"
    document.getElementById("end_call_button").addEventListener("click", function() {
        console.log("Botón 'Terminar Llamada' clickeado.");
        fetch("/end_call", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(response => {
            console.log("Respuesta recibida del servidor.");
            return response.json();
        })
        .then(data => {
            if (data.result === "ok") {
                console.log("Informe recibido:", data.informe);
                const informe = data.informe;
                document.getElementById("total_palabras").innerText = informe.Costos_Estimados.Total_Palabras;
                document.getElementById("total_tokens").innerText = informe.Costos_Estimados.Total_Tokens;
                document.getElementById("costo_total").innerText = informe.Costos_Estimados.Costo_Total;
                document.getElementById("sentimiento_detectado").innerText = informe.Sentimiento_Detectado;
                document.getElementById("emociones_dominantes").innerText = informe.Emociones_Dominantes.join(", ");
                document.getElementById("indicador_negociacion").innerText = informe.Indicador_Negociacion;
            } else {
                console.error("Error al generar el informe:", data.message);
                alert("Error al generar el informe: " + data.message);
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
    });
});