import {
    imagePreview,
    loadRecord,
    setValue,
    showNotFound,
    updateRecord
} from "../../utils/helpers.js"

export async function brandUpdatePage(params) {
    const id = params.get("id")
    const main = document.getElementById("main-content")
    const response = await fetch("pages/brand/update.html")

    main.innerHTML = await response.text()

    const brand = await loadRecord("brand", id)

    if (!brand) {
        showNotFound(main)
        return
    }

    document.getElementById("brandId").value = brand.id
    setValue("name", brand.name)
    setValue("email", brand.email)
    setValue("phone", brand.phone)
    setValue("address", brand.address)
    setValue("status", brand.status)
    imagePreview("imagePreview", brand.logo)

    const form = document.getElementById("submitForm")

    form.addEventListener("submit", (event) => {
        event.preventDefault()
        updateRecord("brand", id, form, "#/brand")
    })
}
