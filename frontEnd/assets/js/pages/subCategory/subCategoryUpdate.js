export async function subCategoryUpdatePage(params){
    let id = params.get("id")

    const subCategoryContent = await fetch("pages/subCategory/update.html")
    const main = document.getElementById("main-content")

    main.innerHTML = await subCategoryContent.text()

    let response = await fetch(`http://127.0.0.1:8000/api/v1/subcategory/?id=${id}`)
    let data = await response.json()
    let subCategory = data.items.find(value => value.id == id)

    if (!subCategory) {
        main.innerHTML = "<p>Sub category not found.</p>"
        return
    }

    const categoryContent = await fetch(`http://127.0.0.1:8000/api/v1/category/`)
    const categoryData = await categoryContent.json()
    const category = categoryData.items.find(value => value.id == subCategory.category_id)

    document.getElementById("categoryId").value = subCategory.id
    document.getElementById("name").value = subCategory.name
    document.getElementById("category_name").value = category ? category.name : ""
    document.getElementById("code").value = subCategory.code
    document.getElementById("description").value = subCategory.description
    document.getElementById("status").value = subCategory.status
    document.getElementById("imagePreview").src = `http://127.0.0.1:5500/${subCategory.icon}`

    let form = document.getElementById("submitForm")
    let message = document.getElementById("message")

    form.addEventListener("submit", async(event) => {
        event.preventDefault()
        message.textContent = ""

        let formData = new FormData(form)

        let response = await fetch(`http://127.0.0.1:8000/api/v1/subcategory/${id}`, {
            method : "PUT",
            body : formData
        })

        if (response.ok){
            window.location.hash = "#/subcategory"
            return
        }
    })
}
