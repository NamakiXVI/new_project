var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
    lineNumbers: true,
    mode: "python",
    theme: "default",
    indentUnit: 4,
});

document.getElementById("execute").addEventListener("click", function() {
    var code = editor.getValue();
    fetch('/execute', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'code': code
        })
    })
    .then(response => response.text())
    .then(data => {
        document.getElementById('output').innerText = data;
    });
});
