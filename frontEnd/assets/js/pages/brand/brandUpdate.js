import {
    loadRecord,
    updateRecord
} from "../../utils/helpers.js"

export async function brandUpdatePage(params) {
    const id = params.get("id")
    
    const main = document.getElementById("main-content")
    const response = await fetch("pages/brand/update.html")

    main.innerHTML = await response.text()

    const brand = await loadRecord("brand", id)

    if (!brand) {
        main.innerHTML = "<p>Category not found.</p>"
        return
    }

    document.getElementById("brandId").value = brand.id
    document.getElementById("name").value = brand.name 
    document.getElementById("email").value = brand.email 
    document.getElementById("phone").value = brand.phone
    document.getElementById("address").value = brand.address 
    document.getElementById("status").value = brand.status 
    document.getElementById("imagePreview").src = `http://127.0.0.1:5500/${brand.logo}`

    const form = document.getElementById("submitForm")

    form.addEventListener("submit", (event) => {
        event.preventDefault()
        updateRecord("brand", id, form, "#/brand")
    })
}
