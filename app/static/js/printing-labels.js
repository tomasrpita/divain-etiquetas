'use strict'

const iptEanBotella = document.getElementById('eanBotella'),
	smallEanBotella = document.getElementById('smallEanBotella'),
	spinnerEanBotella = document.getElementById('spinnerEanBotella'),
	divHiddenInputs = document.getElementById('hiddenInputs'),
	iptLoteBotella = document.getElementById('loteBotella'),
	formLabels = document.getElementById('myForm'),
	checkD100 = document.getElementById('tscLabel1');

const divBotellas = document.querySelector('#divBotellas')
const divBottles = divBotellas.querySelectorAll('span')
const showBottleImp = document.querySelector('.show-bottle')
const hiddeBottleImp = document.querySelectorAll('.hidde-bottle')

const iptCaja = document.getElementById('caja');
const iptTapon = document.getElementById('tapon');
const iptEtiqueta = document.getElementById('etiqueta');

const chksImpresora1 = document.querySelectorAll('#impresora-1 input[type="radio"]');
const chksImpresora2 = document.querySelectorAll('#impresora-1 input[type="radio"]');
const chkCodigoBarras = document.getElementById('zdLabel1');


chksImpresora1.forEach(chk => {
	chk.addEventListener('change', () => {
		if (chk.checked && chk.value == 'sample') {
			document.querySelector('#sample2').disabled = false;
			document.querySelector('#sample3').disabled = false;
		} else {
			document.querySelector('#sample2').disabled = true;
			document.querySelector('#sample3').disabled = true;
		}
	})
})




let divain100 = false
let firstBottle = true
let divainId100 = ''

if (checkD100.checked) {
	divBottles.forEach(bottle => { bottle.classList.remove('invisible') })
	divain100 = true
}

hiddeBottleImp.forEach(bottle => {
	bottle.addEventListener('change', function () {
		if (this.checked) {
			divBottles.forEach(bottle => { bottle.classList.add('invisible') })
			divain100 = false
		}


	})
})


showBottleImp.addEventListener('change', function () {
	if (this.checked) {
		divBottles.forEach(bottle => { bottle.classList.remove('invisible') })
		divain100 = true
	}



})




iptEanBotella.addEventListener('keyup', ({ key }) => {
	if (key === "Enter") {
		if (divain100 && firstBottle) {
			getReference();
		} else if (divain100 && !firstBottle) {
			// getLastBottle()
			if (iptEanBotella.value == divainId100) {
				divBottles.forEach((bottle, i) => {
					if (i == 1) {
						bottle.classList.remove('text-muted')
						bottle.classList.add('text-success')
					}

					iptEanBotella.readOnly = true
					iptLoteBotella.readOnly = false;
					iptLoteBotella.focus();

				})

			}
		} else {
			getReference();
		}

	}
})







iptLoteBotella.addEventListener('keyup', ({ key }) => {
	if (key === "Enter") {
		if (!!iptLoteBotella.value && iptLoteBotella.value.replace(/\s/g, '').length)
			formLabels.submit()
	}
})


const getlastBottle = () => {
	if (iptEanBotella.value == divainId100) {
		divBottles.forEach((bottle, i) => {
			if (i == 1) {
				bottle.classList.remove('text-muted')
				bottle.classList.add('text-success')
			}


			iptLoteBotella.readOnly = false;
			iptLoteBotella.focus();



		})

	}

}


const getReference = () => {
	console.log('getReference')
	spinnerEanBotella.classList.remove('invisible');
	const eanBotella = iptEanBotella.value;
	getData(`/api/reference/${eanBotella}`)
		.then(result => {
			console.log(result);
			if (!!result.data) {
				// console.log(result.data);
				postReferenceData(result.data)
				selectLabel(result.data)
				iptEanBotella.classList.remove("is-invalid");
				iptEanBotella.classList.add("is-valid");

				// console.log("divian100", divain100)
				if (!divain100)
					iptEanBotella.readOnly = true;
					// si tengo que imprimir el código de barras pido el lote
					if (chkCodigoBarras.checked) {
						iptLoteBotella.readOnly = false;
						iptLoteBotella.focus();
					}
				else {
					firstBottle = false
					divainId100 = iptEanBotella.value
					iptEanBotella.value = ''
					divBottles.forEach((bottle, i) => {
						if (i == 0) {
							bottle.classList.remove('text-muted')
							bottle.classList.add('text-success')
						}

					})
				}

				// if (result.data.categoria == 'black')
				// 	iptEanBotella.value += '        =>              !!!!!BLACK!!!!!';

				
				// if (!checkD100.checked)
					// formLabels.submit();

			} else if (!!result.error) {
				throw new Error(result.error)
			} else {
				throw new Error('Error desconocido')
			}

		}).catch((err) => {
			console.error(err);
			showErrorAlert('Error al obtener la referencia: ' + err);
		}).finally(() => spinnerEanBotella.classList.add('invisible'))
}

const postReferenceData = ({ ean_botes, ean_muestras, numero_divain, sexo, sku, categoria, tapon, caja, ingredientes }) => {

	iptTapon.value = tapon || '';
	iptCaja.value = caja || '';

	let hiddenInputs = `
    <input type="text" name="ean_botes" value="${ean_botes}">
	<input type="text" name="ean_muestras" value="${ean_muestras}">
    <input type="text" name="numero_divain" value="${numero_divain}">
    <input type="text" name="sexo" value="${sexo}">
    <input type="text" name="sku" value="${sku}">
	<input type="text" name="categoria" value="${categoria}">
    `
	hiddenInputs += ingredientes ?
		`<input type="text" name="ingredientes" value="${ingredientes}">`
		: '';

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

const selectLabel = ({ categoria, sexo }) => {

	console.log('selectLabel');
	console.log({ categoria }, { sexo }, { chk: getChkValue(chksImpresora1) })


	// Bottle es DIVAIN 100 (100ml)
	if (getChkValue(chksImpresora1) == 'bottle') {

		if (categoria == 'divain') {

			// Misma impresión Solo NUmeros Centrados
			// file: syandard_100ml
			// ETIQUETA Standard Femme
			// 8436592101047
			if (sexo == 'F E M M E') {
				iptEtiqueta.value = 'ESTANDAR - FEMME';
				// ETIQUETA Standard Homme
				// 8436596740037
			} else if (sexo == 'H O M M E') {
				iptEtiqueta.value = 'ESTANDAR - HOMME';
				// ETIQUETA Standard Unisex
				//8436596741287
			} else if (sexo == 'U N I S E X') {
				iptEtiqueta.value = 'ESTANDAR - UNISEX';


				// ETIQUETA kids
				// Una Sola Etiqueta
				// debe imprimir: número, raya, sexo y lote (centrado).
				// file: xHacer
				// 8436592109036
			}
			else if (sexo == 'K I D S') {
				iptEtiqueta.value = 'KIDS';

			}


			// Una etiqueta que puede ser BLACK_EDITION_HOMME, BLACK_EDITION_FEMME, BLACK_EDITION_UNISEX
			// debe imprimir: número, raya y sexo (centrado).
			// file: xHacer
			// 8436592102969
		} else if (categoria == 'black') {
			iptEtiqueta.value = 'BLACK EDITION';

			// ETIQUETA SOLIDARIO_UNISEX
			// Debe imprimir: número, raya y sexo (centrado).
			// file: xHacer
			// 8436592109937
		} else if (categoria == 'solidario') {
			iptEtiqueta.value = 'SOLIDARIO UNISEX';

		}

	}

}

const getChkValue = (chks) => {
	for (let i = 0; i < chks.length; i++) {
		if (chks[i].checked)
			return chks[i].value;
	}
	return null;
}

