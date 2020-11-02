'use strict'

const iptUbicacion = document.getElementById('iptUbicacion'),
      iptIdLocation = document.getElementById('iptIdLocation'),
      iptCodigo = document.getElementById('iptCodigo'),
      smallCodigo = document.getElementById('smallCodigo'),
      iptSKU = document.getElementById('iptSKU'),
      spinnerCodigo = document.getElementById('spinnerCodigo'),
      divIdReference = document.getElementById('divIdReference'),
      spinnerUbicacion = document.getElementById('spinnerUbicacion');

let confirmUbicacion;


iptUbicacion.addEventListener('keyup', ({key}) => {
    if (key === "Enter"){
        iptUbicacion.setAttribute('readonly', 'true')
        getLocation();

    }

    })

iptCodigo.addEventListener('keyup', ({key}) => {
        if (key === "Enter") {
            // getReference();
            iptCodigo.setAttribute('readonly', 'true');
            checkReference();
        }
    })

const getLocation = () => {
        spinnerUbicacion.classList.remove('invisible');
        getData(`/api/location/${iptUbicacion.value}`)
        .then(({id}) => {
            if (id) {
                iptIdLocation.value = id;
                iptUbicacion.classList.remove("is-invalid");
                iptUbicacion.classList.add("is-valid");
                // iptUbicacion.setAttribute('readonly', 'true')
                smallUbicacion.classList.add('invisible')
                iptCodigo.removeAttribute("readonly");
                iptCodigo.focus();
            } else {
                iptUbicacion.classList.add("is-invalid");
                smallUbicacion.classList.remove('invisible')
                iptUbicacion.removeAttribute("readonly");
                iptUbicacion.value = ""
                audioPlay('wrong');
            };
        })
        .catch(error => {
            // TODO arregla esto en el lado server
            console.log(error);
        }).finally(() => {
            // iptCodigo.setAttribute('readonly', 'false');
            spinnerUbicacion.classList.add('invisible');
            // document.getElementById("formAlmacenaje").submit();
            }
        )
}

const checkReference = () => {
    if (iptCodigo.value === iptUbicacion.value) {
        // console.log("Se confirma la ubicacion se hace la auditoria");
        // iptCodigo.setAttribute('readonly', 'true');
        iptCodigo.classList.remove("is-invalid");
        iptCodigo.classList.add("is-valid");
        smallCodigo.classList.add('invisible')
        sessionStorage.setItem('success','true');
        document.getElementById("formAudit").submit();

    } else {
        getReference();
    }
}

const getReference = () => {
    spinnerCodigo.classList.remove('invisible');
    getData(`/api/reference/${iptCodigo.value}`)
    .then(({id, sku}) => {
        if (id) {
            iptSKU.value = sku;
            // iptIdReference.value = id;
            iptCodigo.classList.remove("is-invalid");
            smallCodigo.classList.add('invisible');
            // iptCodigo.classList.add("is-valid");
            // iptCodigo.setAttribute('readonly', 'true');
            // iptUbicacion.removeAttribute("readonly");
            // iptUbicacion.focus();
            appendReferenceId(id);
            confirmReferenceRead();
            iptCodigo.value = ""
            iptCodigo.removeAttribute("readonly");



        } else {
            iptCodigo.classList.add("is-invalid");
            smallCodigo.classList.remove('invisible')
            iptCodigo.value = ""
            iptCodigo.removeAttribute("readonly");
            audioPlay('wrong');
        };
    }

    )
    .catch(error => {
        // TODO arregla esto en el lado server
        console.log(error);
    }).finally(() => spinnerCodigo.classList.add('invisible'))
}

const confirmReferenceRead = () => {
    const panelmessages = document.getElementById('panelmessages');
    const message = `
    <div class="alert alert-success alert-dismissible fade show" role="alert">
        Lectura de referencia <strong>${iptSKU.value}</strong> exitosa!
        <button type="button" class="close" data-dismiss="alert" aria-label="Cerrar">
            <span aria-hidden="true">&times;</span>
        </button>
    </div>
    `
    panelmessages.innerHTML += message;
}

const appendReferenceId = (id_reference) => {
    const iptIdReference = `
        <input type='hidden' name='id_reference[]' value='${id_reference}'/>
        `
    divIdReference.innerHTML += iptIdReference;
}
