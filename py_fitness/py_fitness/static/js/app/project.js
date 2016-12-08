var rome = require('rome');

var datepicker = document.getElementById('id_date');
var timepicker = document.getElementById('id_duration');

if (datepicker) {
  rome(datepicker);
}


if (timepicker) {
  rome(timepicker, { date: false });
}
