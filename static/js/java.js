function compileExecute() {
    var code = document.getElementById('code').value;
    fetch('/compile_execute', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'code=' + encodeURIComponent(code)
    })
    .then(response => response.text())
    .then(data => {
        document.getElementById('output').innerText = data;
    });
}

function updateLineNumbers() {
    var textarea = document.getElementById('code');
    var lineNumbers = document.getElementById('line-numbers');
    var lines = textarea.value.split('\n').length;
    lineNumbers.innerHTML = '';
    for (var i = 1; i <= lines; i++) {
        lineNumbers.innerHTML += i + '<br>';
    }
}
