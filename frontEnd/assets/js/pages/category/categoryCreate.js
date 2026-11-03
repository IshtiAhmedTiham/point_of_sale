function errorText(error, fallback) {
    if (typeof error.detail === "string") return error.detail
    if (Array.isArray(error.detail)) return error.detail.map((item) => item.msg).join(", ")
    return fallback
}

export async function categoryCreatePage() {
    let categoryContent = await fetch("pages/category/create.html")

    let main = document.getElementById("main-content")
    main.innerHTML = await categoryContent.text()

    let form = document.getElementById("submitForm")
    let message = document.getElementById("message")
    let submitButton = document.getElementById("submitButton")

    form.addEventListener("submit", async (event) => {
        event.preventDefault()

        submitButton.disabled = true
        message.textContent = ""

        try {
            let formData = new FormData(form)

            let response = await fetch("http://127.0.0.1:8000/api/v1/category/", {
                method: "POST",
                body: formData
            })

            if (!response.ok) {
                let error = await response.json().catch(() => ({}))
                message.textContent = errorText(error, "Category creation failed")
                return
            }

            window.location.hash = "#/category"
        } finally {
            submitButton.disabled = false
        }
    })
}
