$(document).ready(function(){
	$('.btn-sideBar-SubMenu').on('click', function(){
		var SubMenu=$(this).next('ul');
		var iconBtn=$(this).children('.zmdi-caret-down');
		if(SubMenu.hasClass('show-sideBar-SubMenu')){
			iconBtn.removeClass('zmdi-hc-rotate-180');
			SubMenu.removeClass('show-sideBar-SubMenu');
		}else{
			iconBtn.addClass('zmdi-hc-rotate-180');
			SubMenu.addClass('show-sideBar-SubMenu');
		}
	});
	$('.btn-exit-system').on('click', function(){
		swal({
		  	title: 'Estas seguro?',
		  	text: "Tu actual sesión se cerrará",
		  	type: 'warning',
		  	showCancelButton: true,
		  	confirmButtonColor: '#03A9F4',
		  	cancelButtonColor: '#F44336',
		  	confirmButtonText: '<i class="glyphicon glyphicon-ok-circle"></i> Yes, Salir!',
		  	cancelButtonText: '<i class="glyphicon glyphicon-remove-circle"></i> No, Cancelar!'
		}).then(function () {
			
			window.location.href="/logout";
		});
	});
	$('.btn-menu-dashboard').on('click', function(){
		var body=$('.dashboard-contentPage');
		var sidebar=$('.dashboard-sideBar');
		if(sidebar.css('pointer-events')=='none'){
			body.removeClass('no-paddin-left');
			sidebar.removeClass('hide-sidebar').addClass('show-sidebar');
		}else{
			body.addClass('no-paddin-left');
			sidebar.addClass('hide-sidebar').removeClass('show-sidebar');
		}
	});
	
	$('.btn-modal-help').on('click', function(){
		$('#Dialog-Help').modal('show');
	});
});
(function($){
    $(window).on("load",function(){
        $(".dashboard-sideBar-ct").mCustomScrollbar({
        	theme:"light-thin",
        	scrollbarPosition: "inside",
        	autoHideScrollbar: true,
        	scrollButtons: {enable: true}
        });
        $(".dashboard-contentPage, .Notifications-body").mCustomScrollbar({
        	theme:"dark-thin",
        	scrollbarPosition: "inside",
        	autoHideScrollbar: true,
        	scrollButtons: {enable: true}
        });
    });
})(jQuery);

function confirmarBorrar() {
	if (confirm("¿Estás seguro de que deseas borrar este dato?")) {
		// aquí llamas a la función para borrar el dato
		borrarDato();
	}
}

function borrarDato() {
	
	fetch('/eliminar_producto', {
		method: 'POST'
	}).then(function(response) {
		return response.json();
	}).then(function(data) {
		alert(data.message);
	}).catch(function(error) {
		console.error(error);
	});
}

document.addEventListener('DOMContentLoaded', function() {
    const eyeIcons = document.querySelectorAll('.eye');
    eyeIcons.forEach(icon => {
        icon.addEventListener('click', function() {
            const passwordField = document.querySelector(this.getAttribute('toggle'));
            this.classList.toggle('active');
            if (passwordField.type === 'password') {
                passwordField.type = 'text';
            } else {
                passwordField.type = 'password';
            }
        });
    });
});