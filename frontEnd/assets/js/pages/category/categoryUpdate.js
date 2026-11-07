import { loadRecord, updateRecord } from "../../utils/helpers.js"

export async function categoryUpdatePage(params) {
    let id = params.get("id")

    let categoryContent = await fetch("pages/category/update.html")
    let main = document.getElementById("main-content")

    main.innerHTML = await categoryContent.text()
    
    let category = await loadRecord("category", id)

    if (!category) {
        main.innerHTML = "<p>Category not found.</p>"
        return
    }


    document.getElementById("categoryId").value = category.id
    document.getElementById("name").value = category.name
    document.getElementById("code").value = category.code
    document.getElementById("description").value = category.description
    document.getElementById("status").value = category.status
    document.getElementById("imagePreview").src = `http://127.0.0.1:5500/${category.icon}`
    

    let form = document.getElementById("submitForm")

    form.addEventListener("submit", async(event) => {
        event.preventDefault()

        updateRecord("category", id, form, "#/category")
    })

}
