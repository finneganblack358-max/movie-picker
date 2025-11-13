function get_catagories() {
    // Event Listeners for buttons here
    // return array of if event listeners are selected
}

let userCatagories = get_catagories()

function save_catagories(user_catagories) {
    let save_button = document.getElementById("saveButton")
    save_button.addEventListener("click", function onClick() {
        // Saving to the api here
        alert("Saved Succsesfully")
    })
}
save_catagories()
