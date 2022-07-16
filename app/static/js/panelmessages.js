'use strict'

const panelmessages = document.getElementById('panelmessages');

// Si estamos en auditoria podemos recibir más de 3 mensajes y nos interesa leerlos
const maxMessagesToShow = window.location.pathname !== "/auditoria/" ? 3 : 100;

// Remueve el primer mensaje de si tenemos mas de maxMessagesToShow
const  removeMessage = () => {
    if (panelmessages.childElementCount > maxMessagesToShow)
        panelmessages.removeChild(panelmessages.firstChild);
};

// Observador para cuando se agregan mensajes al panel del lado cliente
const config = { childList: true};
const callback = function(mutationsList, observer) {
    for(let mutation of mutationsList) {
        if (mutation.type === 'childList') {
            removeMessage();
        }
    }
};
const observer = new MutationObserver(callback);
observer.observe(panelmessages, config);

// ejecuta la función cuando venimos con posibles mensajes del lado servisor
removeMessage();