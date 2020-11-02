'use strict'

const btnTextSearch = document.querySelector("#btnTextSearch");

const  pagetoOneAndSubmit = () =>  {
    document.querySelector("#iptPage").value = 1;
    document.querySelector("#formInventario").submit();
}

btnTextSearch.addEventListener('click', () => {
    pagetoOneAndSubmit();
})