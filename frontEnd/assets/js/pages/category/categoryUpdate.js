export async function categoryUpdatePage(params) {
    let id = params.get("id")

    let categoryContent = await fetch("pages/category/update.html")
    let main = document.getElementById("main-content")

    main.innerHTML = await categoryContent.text()
    
    let response = await fetch(`http://127.0.0.1:8000/api/v1/category/?id=${id}`)
    let data = await response.json()
    let category = data.items.find(value => value.id == id)

    document.getElementById("categoryId").value = category.id
    document.getElementById("name").value = category.name
    document.getElementById("code").value = category.code
    document.getElementById("description").value = category.description
    document.getElementById("status").value = category.status
    document.getElementById("imagePreview").src = `http://127.0.0.1:5500/${category.icon}`
    

    let form = document.getElementById("submitForm")

    form.addEventListener("submit", async(event) => {
        event.preventDefault()

        let formData = new FormData(form)
    
        let response = await fetch(`http://127.0.0.1:8000/api/v1/category/${id}`, {
            method : "PUT",
            body : formData
        })

        window.location.hash = "#/category"
    })

}
