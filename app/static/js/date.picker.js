'use strict'

const picker = new Lightpick({
    field: document.getElementById('datepicker'),
    singleDate: false,
    lang: 'es',
    onSelect: function(start, end){

        document.getElementById('date_start').value = start.format("Y-MM-DD");
        document.getElementById('date_end').value = end.format("Y-MM-DD");
    }
    });

const date_start = document.getElementById('date_start').value,
        date_end   = document.getElementById('date_end').value;

if (date_start && date_end)
    picker.setDateRange(date_start, date_end);