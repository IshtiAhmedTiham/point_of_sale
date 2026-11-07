export async function subCategoryCratePage() {
    let categoryContent = await fetch("pages/subCategory/create.html")

    let main = document.getElementById("main-content")
    main.innerHTML = await categoryContent.text()

    let form = document.getElementById("submitForm")

    form.addEventListener("submit", async (event) => {
        event.preventDefault()

        let formData = new FormData(form)

        let response = await fetch("http://127.0.0.1:8000/api/v1/subcategory", {
            method: "POST",
            body: formData
        })

        if (response.ok) {
            window.location.hash = "#/subcategory"  
        }
    })
}
