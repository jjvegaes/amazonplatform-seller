/* Set the width of the sidebar to 250px and the left margin of the page content to 250px */
function openNav() {
  document.getElementById("mySidebar").style.width = "250px";
  document.getElementById("main").style.marginLeft = "250px";
}

/* Set the width of the sidebar to 0 and the left margin of the page content to 0 */
function closeNav() {
  document.getElementById("mySidebar").style.width = "0";
  document.getElementById("main").style.marginLeft = "0";
}

$(function () {
        $("#from").datepicker({
        onClose: function (selectedDate) {
        $("#to").datepicker("option", "minDate", selectedDate);
        }
        });
        $("#to").datepicker({
        onClose: function (selectedDate) {
        $("#from").datepicker("option", "maxDate", selectedDate);
        }
        });
        });


$(function () {
        $.datepicker.setDefaults($.datepicker.regional["es"]);
        $("#from").datepicker({
        minDate: "-20D",
        maxDate: "+2M, -10D"
        });
        });