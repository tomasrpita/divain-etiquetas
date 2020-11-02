'use strict'

const iptCodigo = document.getElementById('iptCodigo'),
      smallCodigo = document.getElementById('smallCodigo'),
      iptSKU = document.getElementById('iptSKU'),
      spinnerCodigo = document.getElementById('spinnerCodigo'),
      iptIdReference = document.getElementById('iptIdReference'),
      iptDateEntry = document.getElementById('iptDateEntry');


let confirmReference = false,
    locationNofound = "",
    confirmCodigo;
      

iptCodigo.addEventListener('keyup', ({key}) => {
        if (key === "Enter") {
            
            if (!confirmReference) {
                confirmCodigo = iptCodigo.value;
                getReference();
            } else {
                unsubscribeReference();
            }
        }
    })

const getReference = (retry=false) => {
        spinnerCodigo.classList.remove('invisible');
        const codigoSearch = retry ? confirmCodigo : iptCodigo.value;
        getData(`/api/reference/${codigoSearch}`)
        .then(({id, sku, availability, location, date_entry}) => {
            if (id) {
                iptSKU.value = sku;
                if (availability) {
                    console.log("Disponible");
                    iptIdReference.value = id;
                    iptDateEntry.value = date_entry;
                    iptCodigo.classList.remove("is-invalid");
                    iptUbicacion.value = location;
                    iptUbicacion.classList.add("is-valid");
                    iptCodigo.value = "";
                    iptCodigo.focus();
                    confirmReference = true;
                    iptCodigo.setAttribute('placeholder', '2 - Reingrese código de la referencia');
                    !!retry && showNextLocationAlert(location);
                    
                } else {
                    console.log("No disponible");
                    showNoavailabilityAlert();
                    iptCodigo.value = ""
                    iptSKU.value = "";
                    iptUbicacion.value = ""
                    iptCodigo.setAttribute('placeholder', '1 - Ingrese código de la referencia');
                    iptCodigo.focus();
                    confirmReference = false
                }
    
            } else {
                console.log("Por que estoy aqui?");
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


const unsubscribeReference = () => {
    if (iptCodigo.value === confirmCodigo) {
        sessionStorage.setItem('success','true');
        document.getElementById("formPicking").submit();
    // A diferencia de picking siempre vamos a suponer que el cartucho esta donde se indica
    // porque el de picking no ira por el, ya sera en la lista d ependientes que lo confirmemos o no.
    } else if (iptCodigo.value === iptUbicacion.value) {
        console.log(iptUbicacion.value);
        console.log(iptCodigo.value);
        locationNofound = iptUbicacion.value
        deleteData('/api/reference-entry/', {id_reference: iptIdReference.value, date_entry: iptDateEntry.value, location_name: iptUbicacion.value })
        .then(() => console.log("Todo Bien"))
        .catch(error => {console.log(error);})
        .finally(() => {getReference(true);});
        
        console.log("No existe aqui, lo eliminamos y damos siguiente ubc");
    } else {
        iptCodigo.classList.add("is-invalid");
        smallCodigo.classList.remove('invisible')
        iptCodigo.value = ""
    }

}

const showNoavailabilityAlert = () => {
    const panelmessages = document.getElementById('panelmessages');
    const message = `
    <div class="alert alert-warning alert-dismissible fade show" role="alert">
        <strong>¡ATENCIÓN!</strong> Referencia <strong>${iptSKU.value}</strong> no disponible en el almacén
        <button type="button" class="close" data-dismiss="alert" aria-label="Cerrar">
            <span aria-hidden="true">&times;</span>
        </button>
    </div>
    `
    panelmessages.innerHTML += message;
}

const showNextLocationAlert = (locationName) => {
    const panelmessages = document.getElementById('panelmessages');
    const message = `
    <div class="alert alert-warning alert-dismissible fade show" role="alert">
        <strong>¡ATENCIÓN!</strong> Ha indicado que no encontro el cartucho ${iptSKU.value} en la ubicación ${locationNofound}, buscar en la nueva ubicación <strong>${locationName}</strong>
        <button type="button" class="close" data-dismiss="alert" aria-label="Cerrar">
            <span aria-hidden="true">&times;</span>
        </button>
    </div>
    `
    panelmessages.innerHTML += message;
}