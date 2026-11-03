function errorText(error, fallback) {
    if (typeof error.detail === "string") return error.detail
    if (Array.isArray(error.detail)) return error.detail.map((item) => item.msg).join(", ")
    return fallback
}

export async function subCategoryCratePage() {
    let categoryContent = await fetch("pages/subCategory/create.html")

    let main = document.getElementById("main-content")
    main.innerHTML = await categoryContent.text()

    let form = document.getElementById("submitForm")
    let message = document.getElementById("message")

    form.addEventListener("submit", async (event) => {
        event.preventDefault()

        message.textContent = ""

        let formData = new FormData(form)

        let response = await fetch("http://127.0.0.1:8000/api/v1/subcategory", {
            method: "POST",
            body: formData
        })

        if (response.ok) {
            window.location.hash = "#/subcategory"
            return
        }

        let error = await response.json().catch(() => ({}))
        message.textContent = errorText(error, "Sub Category creation failed")
    })
}
