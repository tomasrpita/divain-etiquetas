
'use strict'



const iptCodigo = document.getElementById('iptCodigo'),
      smallCodigo = document.getElementById('smallCodigo'),
      iptSKU = document.getElementById('iptSKU'),
      iptUbicacion = document.getElementById('iptUbicacion'),
      spinnerCodigo = document.getElementById('spinnerCodigo'),
      spinnerUbicacion = document.getElementById('spinnerUbicacion'),
      iptIdReference = document.getElementById('iptIdReference'),
      iptIdLocation = document.getElementById('iptIdLocation');


iptCodigo.addEventListener('keyup', ({key}) => {
    if (key === "Enter") {
        getReference();
        
    }
})

iptUbicacion.addEventListener('keyup', ({key}) => {
    if (key === "Enter")
        getLocation();
})


const getReference = () => {
    spinnerCodigo.classList.remove('invisible');
    getData(`/api/reference/${iptCodigo.value}`)
    .then(({id, sku}) => {
        if (id) {
            iptSKU.value = sku;
            iptIdReference.value = id;
            iptCodigo.classList.remove("is-invalid");
            iptCodigo.classList.add("is-valid");
            iptCodigo.setAttribute('readonly', 'true');
            smallCodigo.classList.add('invisible');
            iptUbicacion.removeAttribute("readonly");
            iptUbicacion.focus();


        } else {
            iptCodigo.classList.add("is-invalid");
            smallCodigo.classList.remove('invisible')
            iptCodigo.value = ""
            audioPlay('wrong');
        };
    }

    )
    .catch(error => {
        // TODO arregla esto en el lado server
        console.log(error);
    }).finally(() => spinnerCodigo.classList.add('invisible'))
}

const getLocation = () => {
    let sucess = false;
    spinnerUbicacion.classList.remove('invisible');
    getData(`/api/location/${iptUbicacion.value}`)
    .then(({id}) => {
        if (id) {
            iptIdLocation.value = id;
            iptUbicacion.classList.remove("is-invalid");
            iptUbicacion.classList.add("is-valid");
            iptUbicacion.setAttribute('readonly', 'true')
            smallUbicacion.classList.add('invisible')
            sucess = true;
        } else {
            iptUbicacion.classList.add("is-invalid");
            smallUbicacion.classList.remove('invisible')
            iptUbicacion.value = ""
            audioPlay('wrong');
        };
    })
    .catch(error => {
        // TODO arregla esto en el lado server
        console.log(error);
    }).finally(() => {
        spinnerUbicacion.classList.add('invisible');
        sessionStorage.setItem('success','true');
        sucess && document.getElementById("formAlmacenaje").submit();
        }
    )
}




