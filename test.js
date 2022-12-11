async function writeAnswers() {
    let user = { name: 'user', password: 'password', email: 'user@ukr.net' };

    let response = await fetch('http://77.120.190.159:5555/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json;charset=utf-8' },
        body: JSON.stringify(user),
    });
    server_answer = await response.text();
    // questions = JSON.parse(json);

    console.log(server_answer);
}
writeAnswers();
