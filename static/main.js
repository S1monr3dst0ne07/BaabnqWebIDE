


var editor = document.getElementById("editor");
var output = document.getElementById("output");




document.getElementById("runButton").addEventListener("click", run);
document.addEventListener("keypress", (e) => {
    if (e.ctrlKey && e.key == "Enter") run();
    
});


function run() {
    
    sendPost({
        'source': editor.innerText
    }, "/run");
    
    updateHighlightTag(editor);
}


function sendPost(data, dest) {
    var http = new XMLHttpRequest();

    http.open('POST', dest);
    http.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');

    http.onreadystatechange = () => {
        if (http.readyState == 4 && http.status == 200)
            setOutput(http.responseText);
    };


    http.send(JSON.stringify(data));
    setOutput("Running ...");
}


function setOutput(msg) {
    output.innerHTML = msg;
}