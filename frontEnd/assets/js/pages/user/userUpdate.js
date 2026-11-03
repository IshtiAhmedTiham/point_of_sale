import {
    imagePreview,
    loadRecord,
    setValue,
    showNotFound,
    updateRecord
} from "../../utils/helpers.js"

export async function userUpdatePage(params) {
    const id = params.get("id")
    const main = document.getElementById("main-content")
    const response = await fetch("pages/user/update.html")

    main.innerHTML = await response.text()

    const user = await loadRecord("user", id)

    if (!user) {
        showNotFound(main)
        return
    }

    document.getElementById("userId").value = user.id
    setValue("name", user.name)
    setValue("email", user.email)
    setValue("role", user.role)
    setValue("branch", user.branch)
    setValue("phone", user.phone)
    setValue("address", user.address)
    setValue("status", user.status)
    imagePreview("imagePreview", user.image)

    const form = document.getElementById("submitForm")

    form.addEventListener("submit", (event) => {
        event.preventDefault()
        updateRecord("user", id, form, "#/user")
    })
}
