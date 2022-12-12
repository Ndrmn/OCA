"use strict";

function findInputs() {
	const nameInput = document.querySelector('.adminName');
	const name = nameInput.value;
	const emailInput = document.querySelector('.adminEmail');
	const email = emailInput.value;
	const passInput = document.querySelector('.adminPass');
	const pass = passInput.value;

	return {
		'name': name,
		'password': pass,
		'email': email
	}
}

async function post() {

	const data = findInputs();

	let response = await fetch('http://77.120.190.159:5555/register', {
	  method: 'POST',
	  headers: {
	  	'Content-Type': 'application/json;charset=utf-8',
	  },
	  body: JSON.stringify( data )
	});

	let result = await response.text();
	console.log(result);
}

const button = document.querySelector('.btn');
button.addEventListener('click', function() {
	post()
});