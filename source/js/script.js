"use strict";

let questions = [];

// let results = {
// 	user: {
// 		name: "Test",
// 		surname: "Test",
// 		dOB: "01.01.2000",
// 		gender: "male",
// 		phone: "+380500000000",
// 		email: "test@test.test",
// 		consent: true
// 	},
// 	data: [-1,0,1,0,1,-1,0,1,0,1] //200
// };

let results = {
	user: "test",
	data: "test"
};



//Generate question cards

async function loadQuestions () {
  let response = await fetch('http://77.120.190.159:5555/api/test', {
  method: 'GET'
  });

  questions = await response.json();

  // console.log(questions);

	const cadrs = document.querySelector('.questions');

	const questionsLength = questions.length;
	for(let i=0;i<questionsLength;i++) {
		cadrs.insertAdjacentHTML(
			"beforeend",
			(`<div class="questions__container container">
				<div class="questions__body shadow q${i+1}">
					<div class="questions__question">
						<div class="questions__qstn">
							<div class="questions__name">
								<p>
									${questions[i]}
								</p>
							</div>
							<div class="questions__variants">
								<div class="questions__yes">
										<input type="radio" name="q${i+1}" value="1"/>
									<p>Да</p>
									</div>
									<div class="questions__dontKnow">
										<input type="radio" name="q${i+1}" value="0"/>
										<p>Не знаю</p>
									</div>
									<div class="questions__no">
										<input type="radio" name="q${i+1}" value="-1" checked/>
										<p>Нет</p>
									</div>
								</div>
							</div>
							<div class="questions__number">
								<p>${i+1}</p>
							</div>
						</div>
					</div>
				</div>
			</div>`)
		);
	};
};

async function postResults() {

	let response = await fetch('http://77.120.190.159:5555/api/test', {
	  method: 'POST',
	  headers: {
	    // 'Content-Type': 'text/plain;charset=UTF-8',
	  	'Content-Type': 'application/json;charset=utf-8',
	  },
	  body: JSON.stringify(results)
	});

	let result = await response.text();
	console.log(result);
}

loadQuestions ();




const submitForm = document.querySelector('form');

const inputs = document.querySelectorAll('.inputs');

submitForm.addEventListener("submit", function (event) {

 	for (const i of inputs) {
		if (i.value == '') {
 		   i.classList.add("red");
 		   error();
 		   event.preventDefault();   
 		}
 	}
	
	inputs[0].addEventListener("focus", function (e) {
		if (inputs[0].classList.contains("red")) {
 				inputs[0].classList.remove("red")
 			}
		})
	inputs[1].addEventListener("focus", function (e) {
		if (inputs[1].classList.contains("red")) {
 				inputs[1].classList.remove("red")
 			}
		})
	inputs[2].addEventListener("focus", function (e) {
		if (inputs[2].classList.contains("red")) {
 				inputs[2].classList.remove("red")
 			}
		})
	inputs[3].addEventListener("focus", function (e) {
		if (inputs[3].classList.contains("red")) {
 				inputs[3].classList.remove("red")
 			}
		})
	inputs[4].addEventListener("focus", function (e) {
		if (inputs[4].classList.contains("red")) {
 				inputs[4].classList.remove("red")
 			}
		})


	const genderRadio = mainForm.gender;
	const genderFrame = document.querySelector('.alignRadio')

	if (genderRadio[0].checked == false && genderRadio[1].checked == false) {
		genderFrame.classList.add('red');
		error();
 		event.preventDefault();
	}

	genderFrame.addEventListener("click", function (e) {
		if (genderFrame.classList.contains("red")) {
 				genderFrame.classList.remove("red")
 			}
		})






for (let n=1;n<=200;n++){
	let questionsCheck = document.querySelectorAll(`input[name="q${n}"]`)
	if (questionsCheck[0].checked == false && questionsCheck[1].checked == false && questionsCheck[2].checked == false) {
			let question = document.querySelector(`.q${n}`)
				question.classList.add('red');
				error();
				event.preventDefault();
	}
}
	
	let redFrame = document.querySelectorAll('.questions__body');
	redFrame.forEach(element => {
		element.addEventListener("click", function (e) {
			if (element.classList.contains("red")) {
 				element.classList.remove("red")
			}
		})	
	});


/////////
	const submitBtn = document.querySelector('.btn');
	submitBtn.addEventListener('click', function() {
			postResults();
	});

//////////











});


















//Error notification function
let snackbar = document.querySelector('.snackbar');

function error() {

	snackbar.style.display = "block";
	
	setTimeout( function() {
		snackbar.style.display = "none";
		}, 2000);
	};


	// const submitBtn = document.querySelector('.btn');
	// submitBtn.addEventListener('click', function() {
	// 		postResults();
	// });