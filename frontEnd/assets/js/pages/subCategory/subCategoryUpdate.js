export async function subCategoryUpdatePage(params){
    let id = params.get("id")

    const subCategoryContent = await fetch("pages/subCategory/update.html")
    const main = document.getElementById("main-content")

    main.innerHTML = await subCategoryContent.text()

    let response = await fetch(`http://127.0.0.1:8000/api/v1/subcategory/?id=${id}`)
    let data = await response.json()
    let subCategory = data.items.find(value => value.id == id)

    document.getElementById("categoryId").value = subCategory.id
    document.getElementById("name").value = subCategory.name
    document.getElementById("category").value = subCategory.category_id
    document.getElementById("code").value = subCategory.code
    document.getElementById("description").value = subCategory.description
    document.getElementById("status").value = subCategory.status
    document.getElementById("imagePreview").src = `http://127.0.0.1:5500/${subCategory.icon}`
    
    let form = document.getElementById("submitForm")

    form.addEventListener("submit", async(event) => {
        event.preventDefault()

        let formData = new FormData(form)
        let response = await fetch(`http://127.0.0.1:8000/api/v1/subcategory/${id}`, {
            method : "PUT",
            body : formData
        })

        if (response){
            alert("Data Successfully Updated")
            window.location.hash = "#/subcategory"
        }else{
            alert("Data Updated Successfully Fail")
        }
    })
}