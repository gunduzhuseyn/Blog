function add_class() {
    var element, name, arr;
    element = document.getElementsByClassName("myDIV");
    name = "mystyle";
    arr = element.className.split(" ");
    if (arr.indexOf(name) == -1) {
        element.className += " " + name;
    }
}

function ($){

}