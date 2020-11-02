/*
* Lbreria de funciones varias
*/

// atajo a home sin importar en que app estes corriendo, se usa para las paginas de error
const  goToURL = () =>  location.href = window.location.origin;

const audioWrong = new Audio(wrongSound);
const audioSuccess = new Audio(successSound);
// se habilita este selector si viene un mensaje warning de la auditoria 
// si es asi reproduciremos sonido wrong
const divWarning = document.querySelector("#warning");


const audioPlay = (soundType) => {
    
    sound = {
        wrong: audioWrong,
        success: audioSuccess
    }
    sound[soundType].play();

}

if (sessionStorage.getItem('success'))
    {
        if (!divWarning)
            audioPlay('success');
        else
            audioPlay('wrong');
        sessionStorage.removeItem('success')
    }