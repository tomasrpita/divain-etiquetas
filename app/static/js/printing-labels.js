'use strict'

const   iptEanBotella = document.getElementById('eanBotella'),
        smallEanBotella = document.getElementById('smallEanBotella'),
        spinnerEanBotella = document.getElementById('spinnerEanBotella'),
        divHiddenInputs = document.getElementById('hiddenInputs'),
        iptLoteBotella = document.getElementById('loteBotella'),
        formLabels = document.getElementById('myForm'),
		checkD100 = document.getElementById('tscLabel1')
        
        ;

const divBotellas = document.querySelector('#divBotellas')


const divBottles = divBotellas.querySelectorAll('span')

const showBottleImp = document.querySelector('.show-bottle')

const hiddeBottleImp = document.querySelectorAll('.hidde-bottle')

let divain100 = false
let firstBottle = true
let divainId100 = ''

if (checkD100.checked) {
	divBottles.forEach(bottle => {bottle.classList.remove('invisible') })
	divain100 = true
}

hiddeBottleImp.forEach(bottle => {
	bottle.addEventListener('change', function() {
	if (this.checked){
		divBottles.forEach(bottle => {bottle.classList.add('invisible') })
		divain100 = false
	}
	
		
	})
})


showBottleImp.addEventListener('change', function() {
	console.log("CHANGE")
	if (this.checked) {
		divBottles.forEach(bottle => {bottle.classList.remove('invisible') })
		divain100 = true
	}
		

		
} ) 




iptEanBotella.addEventListener('keyup', ({key}) => {
    if (key === "Enter") {
		if (divain100 && firstBottle) {
			console.log(1)
			getReference();
		} else if (divain100 && !firstBottle) {
			console.log(2)
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
			console.log(3)
			getReference();
		}
        
    }
})







iptLoteBotella.addEventListener('keyup', ({key}) => {
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
    spinnerEanBotella.classList.remove('invisible');
    const eanBotella = iptEanBotella.value;
    getData(`/api/reference/${eanBotella}`)
    .then((result) => {
        // console.log(result);
        if (!!result.data) {
            //console.log("Data");
            console.log(result.data);
            postReferenceData(result.data)
            iptEanBotella.classList.remove("is-invalid");
            iptEanBotella.classList.add("is-valid");
			
			console.log("divian100", divain100)
			if (!divain100)
			    iptEanBotella.readOnly = true;
			else  {
				firstBottle = false
				divainId100 = iptEanBotella.value
				iptEanBotella.value = ''
				divBottles.forEach((bottle, i) => {
					console.log("Hola")
					if (i == 0) {
						bottle.classList.remove('text-muted')
						bottle.classList.add('text-success')
					}
					
					})

			}
			

			if (result.data.categoria == 'black')
				iptEanBotella.value += '        =>              !!!!!BLACK!!!!!';
            
			if (!checkD100.checked)
				formLabels.submit();
			

				
			




        } else if (!!result.error) {
            showErrorAlert(result.error);
        } else {
            console.error("Error Desconocido");
        }
        
    }).catch((err) => {
        
    }).finally(() => spinnerEanBotella.classList.add('invisible'))
}

const postReferenceData = ({ean_botes, ean_muestras, numero_divain, sexo, sku, categoria}) =>  {
    console.log("post");
    const hiddenInputs = `
    <input type="text" name="ean_botes" value="${ean_botes}">
	<input type="text" name="ean_muestras" value="${ean_muestras}">
    <input type="text" name="numero_divain" value="${numero_divain}">
    <input type="text" name="sexo" value="${sexo}">
    <input type="text" name="sku" value="${sku}">
	<input type="text" name="categoria" value="${categoria}">
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