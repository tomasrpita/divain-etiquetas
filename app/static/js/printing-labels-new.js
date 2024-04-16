"use strict";

const iptEanBotella = document.getElementById("eanBotella"),
  smallEanBotella = document.getElementById("smallEanBotella"),
  spinnerEanBotella = document.getElementById("spinnerEanBotella"),
  divHiddenInputs = document.getElementById("hiddenInputs"),
  iptLoteBotella = document.getElementById("loteBotella"),
  formLabels = document.getElementById("myForm"),
  checkD100 = document.getElementById("tscLabel1");

const divBotellas = document.querySelector("#divBotellas");
const divBottles = divBotellas.querySelectorAll("span");
const showBottleImp = document.querySelector(".show-bottle");
const hiddeBottleImp = document.querySelectorAll(".hidde-bottle");

const iptCaja = document.getElementById("caja");
const iptTapon = document.getElementById("tapon");
const iptEtiqueta = document.getElementById("etiqueta");

const chksImpresora1 = document.querySelectorAll(
  '#impresora-1 input[type="radio"]'
);
const chksImpresora2 = document.querySelectorAll(
  '#impresora-2 input[type="radio"]'
);

const chkCodigoBarras = document.getElementById("zdLabel1");

chksImpresora1.forEach((chk) => {
  chk.addEventListener("change", () => {
    if (chk.checked && chk.value == "sample") {
      document.querySelector("#sample2").disabled = false;
      document.querySelector("#sample3").disabled = false;
    } else {
      document.querySelector("#sample2").disabled = true;
      document.querySelector("#sample3").disabled = true;
    }
  });
});

// Controla las etiquetas de destino
const labelsDestination = document.querySelectorAll(
  'input[name="label_destination"]'
);

// Si la impresora 2 es "ninguna" deshabilita las etiquetas de destino
chksImpresora2.forEach((chk) => {
  chk.addEventListener("change", () => {
    if (chk.checked && chk.value == "ninguna") {
      labelsDestination.forEach((label) => {
        label.disabled = true;
      });
    } else {
      labelsDestination.forEach((label) => {
        label.disabled = false;
      });
    }
  });
});

let divain100 = false;
let firstBottle = true;
let divainId100 = "";

if (checkD100.checked) {
  divBottles.forEach((bottle) => {
    bottle.classList.remove("invisible");
  });
  divain100 = true;
}

hiddeBottleImp.forEach((bottle) => {
  bottle.addEventListener("change", function () {
    if (this.checked) {
      divBottles.forEach((bottle) => {
        bottle.classList.add("invisible");
      });
      divain100 = false;
    }
  });
});

showBottleImp.addEventListener("change", function () {
  if (this.checked) {
    divBottles.forEach((bottle) => {
      bottle.classList.remove("invisible");
    });
    divain100 = true;
  }
});

iptEanBotella.addEventListener("keyup", ({ key }) => {
  if (key === "Enter") {
    if (divain100 && firstBottle) {
      console.log("divain100");
      getReference();
    } else if (divain100 && !firstBottle) {
      console.log("divain100 2");
      // getLastBottle()
      if (getEan13(iptEanBotella.value) == divainId100) {
        divBottles.forEach((bottle, i) => {
          if (i == 1) {
            bottle.classList.remove("text-muted");
            bottle.classList.add("text-success");
          }
          iptEanBotella.readOnly = true;
          iptLoteBotella.readOnly = false;
          iptLoteBotella.focus();
        });
      }
    } else {
      console.log("divain1");
      getReference();
    }
  }
});

iptLoteBotella.addEventListener("keyup", ({ key }) => {
  if (key === "Enter") {
    if (
      !!iptLoteBotella.value &&
      iptLoteBotella.value.replace(/\s/g, "").length
    )
      formLabels.submit();
  }
});

const getReference = () => {
  console.log("getReference");
  spinnerEanBotella.classList.remove("invisible");
  const eanBotella = getEan13(iptEanBotella.value);
  const labelInfo = findLabelInfo(eanBotella);

  console.log({ labelInfo });

  if (labelInfo) {
    postReferenceData(labelInfo);
    selectLabel(labelInfo);
    iptEanBotella.classList.remove("is-invalid");
    iptEanBotella.classList.add("is-valid");

    if (!divain100) {
      iptEanBotella.readOnly = true;
      // si tengo que imprimir el código de barras pido el lote
      if (chkCodigoBarras.checked) {
        console.log("chkCodigoBarras:" + chkCodigoBarras.checked);
        iptLoteBotella.readOnly = false;
        iptLoteBotella.focus();
      } else {
        // si no tengo que imprimir el código de barras envío el formulario
        // Caso Sample
        formLabels.submit();
      }
    } else {
      firstBottle = false;
      divainId100 = getEan13(iptEanBotella.value);
      iptEanBotella.value = "";
      divBottles.forEach((bottle, i) => {
        if (i == 0) {
          bottle.classList.remove("text-muted");
          bottle.classList.add("text-success");
        }
      });
    }
  } else {
    console.log("getReference else");
    showErrorAlert(
      "No se ha encontrado la información de la etiqueta con los datos introducidos"
    );
  }

  spinnerEanBotella.classList.add("invisible");
};

const postReferenceData = ({
  ean_bottle,
  ean_sample,
  divain_number,
  sex,
  sku_divain,
  category,
  cap,
  box,
  ingredients,
  fragance_name,
}) => {
  iptTapon.value = cap || "";
  iptCaja.value = box || "";

  let hiddenInputs = `
    <input type="text" name="ean_botes" value="${ean_bottle}">
	<input type="text" name="ean_muestras" value="${ean_sample}">
    <input type="text" name="numero_divain" value="${divain_number}">
    <input type="text" name="sexo" value="${sex}">
    <input type="text" name="sku" value="${sku_divain}">
	<input type="text" name="categoria" value="${category}">
	<input type="text" name="ingredientes" value="${ingredients}">
	<input type="text" name="fragance_name" value="${fragance_name}">

    `;

  divHiddenInputs.innerHTML = hiddenInputs;
};

const showErrorAlert = (errorMessasge) => {
  const panelmessages = document.getElementById("panelmessages");
  const message = `
    <div class="alert alert-warning alert-dismissible fade show" role="alert">
        <strong>¡ATENCIÓN!</strong> ${errorMessasge}
        <button type="button" class="close" data-dismiss="alert" aria-label="Cerrar">
            <span aria-hidden="true">&times;</span>
        </button>
    </div>
    `;
  panelmessages.innerHTML += message;
};

const selectLabel = ({ category, sex }) => {
  console.log("selectLabel");
  console.log({ category }, { sex }, { chk: getChkValue(chksImpresora1) });

  // Bottle es DIVAIN 100 (100ml)
  if (getChkValue(chksImpresora1) == "bottle") {
    if (category == "divain") {
      // Misma impresión Solo NUmeros Centrados
      // file: syandard_100ml
      // ETIQUETA Standard Femme
      // 8436592101047
      if (sex == "F E M M E") {
        iptEtiqueta.value = "ESTANDAR - FEMME";
        // ETIQUETA Standard Homme
        // 8436596740037
      } else if (sex == "H O M M E") {
        iptEtiqueta.value = "ESTANDAR - HOMME";
        // ETIQUETA Standard Unisex
        //8436596741287
      } else if (sex == "U N I S E X") {
        iptEtiqueta.value = "ESTANDAR - UNISEX";

        // ETIQUETA kids
        // Una Sola Etiqueta
        // debe imprimir: número, raya, sex y lote (centrado).
        // file: xHacer
        // 8436592109036
      } else if (sex == "K I D S") {
        iptEtiqueta.value = "KIDS";
      }

      // Una etiqueta que puede ser BLACK_EDITION_HOMME, BLACK_EDITION_FEMME, BLACK_EDITION_UNISEX
      // debe imprimir: número, raya y sex (centrado).
      // file: xHacer
      // 8436592102969
    } else if (category == "black") {
      iptEtiqueta.value = "BLACK EDITION";

      // ETIQUETA SOLIDARIO_UNISEX
      // Debe imprimir: número, raya y sex (centrado).
      // file: xHacer
      // 8436592109937
    } else if (category == "solidario") {
      iptEtiqueta.value = "SOLIDARIO UNISEX";
    }
  }
};

const getChkValue = (chks) => {
  for (let i = 0; i < chks.length; i++) {
    if (chks[i].checked) return chks[i].value;
  }
  return null;
};
