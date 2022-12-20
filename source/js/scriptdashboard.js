"use strict";

async function getUsers() {

	let response = await fetch('http://77.120.190.159:5555/api/get_users', {

	  method: 'GET'
	});

	const result = await response.json();
	console.log(result);

	const table = document.querySelector('.users');

	const galery = document.querySelector('.galery');
	const image = document.querySelector('.galeryImage');
	const btnX = document.querySelector('.closeBtn');

	btnX.addEventListener('click', function() {
		galery.classList.add('hideLoadCircle');
	});

	for (let i = 0; i < result.length; i++) {
		table.insertAdjacentHTML(
			'beforeend',
			`<tr>
				<th scope="row">${i}</th>
				<td>${result[i].name}</td>
				<td>${result[i].surname}</td>
				<td>${result[i].dateofbirth}</td>
				<td>${result[i].phone}</td>
				<td>${result[i].email}</td>
				<td>${result[i].date_of_testing}</td>
				<td><a class="btn btn-primary gal${result[i].id}" href="" role="button">&#128269;</a>
				<a class="btn btn-success" href="http://77.120.190.159:5555/api/get_test_graph/${result[i].id}" role="button">&#129095;</a></td>
			</tr>`
		);
		
		let btn = document.querySelector(`.gal${result[i].id}`);
		btn.addEventListener('click', function() {
			galery.classList.remove('hideLoadCircle');
			image.src = `http://77.120.190.159:5555/api/get_test_graph/${result[i].id}`;
		});
	};
};

getUsers();

