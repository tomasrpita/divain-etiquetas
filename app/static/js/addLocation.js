'use strict'

const btnSaveLocation = document.querySelector('#btnSaveLocation'),
      iptGaps = document.querySelector('#iptGaps'),
      iptUbicacion = document.querySelector('#iptUbicacion');

const errorInputLocation = (errorType) => {
    const errorsMessages = {
        existingLocation: 'Ubicación existente, intente otro nombre',
        invalidFormat: 'Formato de ubicación erróneo, ejemplo formato valido: “01A01”'
    }
    smallUbicacion.innerText = errorsMessages[errorType];
    iptUbicacion.classList.add("is-invalid");
    smallUbicacion.classList.remove('invisible')
    iptUbicacion.value = ""
}

const getLocation = () => {
spinnerUbicacion.classList.remove('invisible');
getData(`/api/location/${iptUbicacion.value}`)
.then(({id}) => {
    if (id) {
        errorInputLocation('existingLocation');
        audioPlay('wrong');
    } else {
        iptUbicacion.classList.remove("is-invalid");
        iptUbicacion.classList.add("is-valid");
        iptUbicacion.setAttribute('readonly', 'true')
        smallUbicacion.classList.add('invisible')
    };
})
.catch(error => {
    // TODO arregla esto en el lado server
    console.log(error);
}).finally(() => {
    spinnerUbicacion.classList.add('invisible');
    })
}

btnSaveLocation.addEventListener('click', () => {
    if (iptGaps.value * 1 === 0) {
        iptGaps.classList.add("is-invalid");
        smallGaps.classList.remove('invisible')
        iptGaps.value = ""
        audioPlay('wrong');
        iptGaps.focus();
    } else {
        sessionStorage.setItem('success','true');
        !!iptUbicacion.value &&  document.getElementById("formAddLocation").submit();
    }})

iptUbicacion.onblur = () => {
    if (iptUbicacion.value.length > 0) {
        const regex = new RegExp("[0-9][0-9][A-Z][0-9][0-9]+");
        if (regex.test(iptUbicacion.value))
            getLocation();
        else
            errorInputLocation('invalidFormat')
    }
}

iptGaps.onkeydown = function(e) {
if(!((e.keyCode > 95 && e.keyCode < 106)
  || (e.keyCode > 47 && e.keyCode < 58)
  || e.keyCode == 8)) {
    return false;
}}