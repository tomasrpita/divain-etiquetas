'use strict'

const   iptEanBotella = document.getElementById('eanBotella'),
        smallEanBotella = document.getElementById('smallEanBotella'),
        spinnerEanBotella = document.getElementById('spinnerEanBotella'),
        divHiddenInputs = document.getElementById('hiddenInputs'),
        iptLoteBotella = document.getElementById('loteBotella'),
        formLabels = document.getElementById('myForm')
        
        ;


iptEanBotella.addEventListener('keyup', ({key}) => {
    if (key === "Enter") {
        getReference();
    }
})

iptLoteBotella.addEventListener('keyup', ({key}) => {
    if (key === "Enter") {
        if (!!iptLoteBotella.value && iptLoteBotella.value.replace(/\s/g, '').length)
            formLabels.submit()
    }
})


const getReference = () => {
    spinnerEanBotella.classList.remove('invisible');
    const eanBotella = iptEanBotella.value;
    getData(`/api/reference/${eanBotella}`)
    .then((result) => {
        // console.log(result);
        if (!!result.data) {
            console.log("if");
            // console.log(result.data);
            postReferenceData(result.data)
            iptEanBotella.classList.remove("is-invalid");
            iptEanBotella.classList.add("is-valid");
            iptEanBotella.readOnly = true;
            iptLoteBotella.readOnly = false;
            iptLoteBotella.focus();



        } else if (!!result.error) {
            showErrorAlert(result.error);
        } else {
            console.error("Error Desconocido");
        }
        
    }).catch((err) => {
        
    }).finally(() => spinnerEanBotella.classList.add('invisible'))
}

const postReferenceData = ({ean_13, numero_divain, sexo, sku}) =>  {
    console.log("post");
    const hiddenInputs = `
    <input type="text" name="ean_13" value="${ean_13}">
    <input type="text" name="numero_divain" value="${numero_divain}">
    <input type="text" name="sexo" value="${sexo}">
    <input type="text" name="sku" value="${sku}">
    `
    divHiddenInputs.innerHTML = hiddenInputs;

}

const showErrorAlert = (errorMessasge) => {
    const panelmessages = document.getElementById('panelmessages');
    const message = `
    <div class="alert alert-warning alert-dismissible fade show" role="alert">
        <strong>¡ATENCIÓN!</strong> ${errorMessasge}
        <button type="button" class="close" data-dismiss="alert" aria-label="Cerrar">
            <span aria-hidden="true">&times;</span>
        </button>
    </div>
    `
    panelmessages.innerHTML += message;
}