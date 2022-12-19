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

	let result = await response.json();
	localStorage.setItem('oca_access_token', result.access_token);
	console.log(localStorage.getItem('oca_access_token'));


	let response2 = await fetch('http://77.120.190.159:5555/test_auth_api', {
	
		method: 'POST',
		headers: {
			'Authorization': `Bearer ${localStorage.getItem('oca_access_token')}`
		}
	});
	let result2 = await response2.text();
	console.log(result2);
}

const button = document.querySelector('.btn');
button.addEventListener('click', function() {
	post()
});