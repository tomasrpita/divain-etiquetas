/*
* Lbreria de funciones varias
*/

// atajo a home sin importar en que app estes corriendo, se usa para las paginas de error
const  goToURL = () =>  location.href = window.location.origin;

const audioWrong = new Audio(wrongSound);
const audioSuccess = new Audio(successSound);
const audioBeep = new Audio(beepSound);
// se habilita este selector si viene un mensaje warning de la auditoria 
// si es asi reproduciremos sonido wrong
const divWarning = document.querySelector("#warning");


const audioPlay = (soundType) => {
    switch (soundType) {
        case "success":
            audioSuccess.play();
            break;
        case "wrong":
            audioWrong.play();
            break;
        case "beep":
            audioBeep.play();
            break;
        default:
            break;
    }
}

if (sessionStorage.getItem('success'))
    {
        if (!divWarning)
            audioPlay('success');
        else
            audioPlay('wrong');
        sessionStorage.removeItem('success')
    }


function convertirFecha(cadenaFechaHora) {
        if (!cadenaFechaHora) {
            return '';
        }
        var fechaHora = new Date(cadenaFechaHora);
        var dia = fechaHora.getDate().toString().padStart(2, '0');
        var mes = (fechaHora.getMonth() + 1).toString().padStart(2, '0');
        var anio = fechaHora.getFullYear().toString();
        var fecha = dia + '-' + mes + '-' + anio;
        return fecha;
    }
    
function parseEan128(ean128) {
        const ean13Pattern = /\(01\)(\d{13})/;
        const batchPattern = /\(10\)(\d+)/;
        const datePattern = /\(17\)(\d{6})/;
    
        const ean13Match = ean128.match(ean13Pattern);
        const batchMatch = ean128.match(batchPattern);
        const dateMatch = ean128.match(datePattern);
    
        const ean13 = ean13Match ? ean13Match[1].substring(1) : null;
        const batch = batchMatch ? batchMatch[1] : null;
        const date = dateMatch ? `${dateMatch[1].substring(0, 2)}-${dateMatch[1].substring(2, 4)}-${dateMatch[1].substring(4, 6)}` : null;
    
        return { ean13, batch, date };
}

const calculateEAN12CheckDigit =  (ean12) => {
    if (ean12.length !== 12 || !/^\d+$/.test(ean12)) {
        throw new Error("Input must be a 12-digit string.");
    }

    let sum = 0;
    for (let i = 0; i < ean12.length; i++) {
        let digit = parseInt(ean12[i]);
        sum += (i % 2 === 0) ? digit : digit * 3;
    }

    let checkDigit = (10 - (sum % 10)) % 10;
    return checkDigit;
}


const getEan13 = (ean128) => {
    console.log("getEan13");
    console.log({ ean128 });

    if (ean128.length == 13) {
        console.log({ ean13: ean128 });
        return ean128;
    }

    // Lista de patrones para buscar el código que empieza con '84' o '87'
    const patterns = [
            /84\d{10}/,
            // /87\d{10}/,
            /\*01\(84\d{10}/,
            // /\*01\(87\d{10}/,
            /01(84\d{10})/,
            // /01(87\d{10})/,
        ];

    for (let pattern of patterns) {
        const match = ean128.match(pattern);
        console.log({ match });
        if (match) {
            const ean12 = match[0];
            const checkDigit = calculateEAN12CheckDigit(ean12);
            const ean13 = ean12 + checkDigit;
            console.log({ ean13 });
            return ean13;
        }
    }

    console.log("No se encontró un EAN13 válido");
    return null;
};
