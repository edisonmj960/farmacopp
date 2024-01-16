const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});

document.addEventListener('DOMContentLoaded', function() {
	const eye = document.querySelector('.eye');
	eye.addEventListener('click', function() {
	  const passwordField = document.querySelector(this.getAttribute('toggle'));
	  this.classList.toggle('active');
	  if (passwordField.type === 'password') {
		passwordField.type = 'text';
	  } else {
		passwordField.type = 'password';
	  }
	});
  });
  


function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    input.type === 'password' ? input.type = 'text' : input.type = 'password';
}

