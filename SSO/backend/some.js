function myfunction() {
    alert("Button has been clicked!")
}
async function load_python() {
    response = await fetch("http://127.0.0.1:5000/")
        .then((response) => response.json())
        .then((json) => console.log(json))
}