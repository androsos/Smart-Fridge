$('.toggle-menu').click (function(){
  	$(this).toggleClass('active');
  	$('#menu').toggleClass('open');



 	var today = new Date();
	var dd = String(today.getDate()).padStart(2, '0');
	var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
	var yyyy = today.getFullYear();

	today = dd + '/' + mm + '/' + yyyy;
	document.getElementById('menu_date').innerHTML = today ;
});


(function () {
    function checkTime(i) {
        return (i < 10) ? "0" + i : i;
    }

    function startTime() {
        var today = new Date(),
            h = checkTime(today.getHours()),
            m = checkTime(today.getMinutes());
        document.getElementById('time').innerHTML = h + ":" + m ;
        t = setTimeout(function () {
            startTime();
        }, 500);
    }
    startTime();
})();