import {
    loadRecord,
    updateRecord
} from "../../utils/helpers.js"

export async function userUpdatePage(params) {
    const id = params.get("id")
    const main = document.getElementById("main-content")
    const response = await fetch("pages/user/update.html")

    main.innerHTML = await response.text()

    const user = await loadRecord("user", id)

    if (!user) {
        main.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-exclamation-circle"></i>
                <strong>Record not found</strong>
                <span>The requested record could not be found.</span>
            </div>
        `
        return
    }

    document.getElementById("userId").value = user.id
    document.getElementById("name").value = user.name ?? ""
    document.getElementById("email").value = user.email ?? ""
    document.getElementById("role").value = user.role ?? ""
    document.getElementById("branch").value = user.branch ?? ""
    document.getElementById("phone").value = user.phone ?? ""
    document.getElementById("address").value = user.address ?? ""
    document.getElementById("status").value = user.status ?? ""
    document.getElementById("imagePreview").src = `http://127.0.0.1:5500/${user.image}`

    const form = document.getElementById("submitForm")

    form.addEventListener("submit", (event) => {
        event.preventDefault()
        updateRecord("user", id, form, "#/user")
    })
}
