async function writeAnswers() {
    let user = { user: 'test user2422', data:'some data' };

    let response = await fetch('http://77.120.190.159:5555/test', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json;charset=utf-8' },
        body: JSON.stringify(user)
    });
    server_answer = await response.text();
    // questions = JSON.parse(json);

    console.log(server_answer);
}
writeAnswers();
