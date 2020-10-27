function copyElementText(id_copy, id_alert) {
    var text = document.getElementById(id_copy).innerText;
    var elem = document.createElement("textarea");
    document.body.appendChild(elem);
    elem.value = text;
    elem.select();
    document.execCommand("copy");
    document.body.removeChild(elem);

    var x = document.getElementById(id_alert);
    x.style.display = "block";
}