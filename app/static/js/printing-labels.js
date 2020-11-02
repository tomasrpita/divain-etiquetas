'use strict'

const   iptEanBotella = document.getElementById('eanBotella'),
        smallEanBotella = document.getElementById('smallEanBotella'),
        spinnerEanBotella = document.getElementById('spinnerEanBotella');

let confirmEanBotella = false;

iptEanBotella.addEventListener('keyup', ({key}) => {
    if (key === "Enter") {
        
        if (!confirmEanBotella) {
            // confirmCodigo = iptCodigo.value;
            getReference();
            console.log("Esta es la data de la referencia");
        } else {
            console.log("pasa al otro campo");
            // unsubscribeReference();
        }
    }
})

const getReference = () => {
    spinnerEanBotella.classList.remove('invisible');
    const eanBotella = iptEanBotella.value;
    getData(`/api/reference/${eanBotella}`)
    .then((result) => {
        console.log(result);
        
    }).catch((err) => {
        
    }).finally(() => spinnerEanBotella.classList.add('invisible'))
}