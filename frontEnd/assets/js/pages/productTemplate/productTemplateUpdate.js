import {
    fetchItems,
    loadRecord,
    updateRecord
} from "../../utils/helpers.js"

export async function productTemplateUpdatePage(params) {
    const id = params.get("id")
    const main = document.getElementById("main-content")
    const response = await fetch("pages/productTemplate/update.html")

    main.innerHTML = await response.text()

    const [productTemplate, categories, subCategories, brands] = await Promise.all([
        loadRecord("product_template", id),
        fetchItems("category"),
        fetchItems("subcategory"),
        fetchItems("brand")
    ])

    if (!productTemplate) {
        main.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-exclamation-circle"></i>
                <strong>Record not found</strong>
                <span>The requested record could not be found.</span>
            </div>
        `
        return
    }

    document.getElementById("productTemplateId").value = productTemplate.id
    document.getElementById("name").value = productTemplate.name ?? ""
    document.getElementById("code").value = productTemplate.code ?? ""
    const categorySelect = document.getElementById("category_name")
    categorySelect.innerHTML = `<option value="">Select category</option>` + categories.map((category) => `
        <option value="${category.name}" ${String(category.id) === String(productTemplate.category_id) ? "selected" : ""}>
            ${category.name}
        </option>
    `).join("")
    const subCategorySelect = document.getElementById("sub_category_name")
    subCategorySelect.innerHTML = `<option value="">Select sub category</option>` + subCategories.map((subCategory) => `
        <option value="${subCategory.name}" ${String(subCategory.id) === String(productTemplate.sub_category_id) ? "selected" : ""}>
            ${subCategory.name}
        </option>
    `).join("")
    const brandSelect = document.getElementById("brand_name")
    brandSelect.innerHTML = `<option value="">Select brand</option>` + brands.map((brand) => `
        <option value="${brand.name}" ${String(brand.id) === String(productTemplate.brand_id) ? "selected" : ""}>
            ${brand.name}
        </option>
    `).join("")
    document.getElementById("mrp").value = productTemplate.mrp ?? ""
    document.getElementById("tax").value = productTemplate.tax ?? ""
    document.getElementById("description").value = productTemplate.description ?? ""
    document.getElementById("openstock").value = productTemplate.openstock ?? ""
    document.getElementById("imagePreview").src = `http://127.0.0.1:5500/${productTemplate.image}`

    const form = document.getElementById("submitForm")

    form.addEventListener("submit", (event) => {
        event.preventDefault()
        updateRecord("product_template", id, form, "#/product_template")
    })
}
