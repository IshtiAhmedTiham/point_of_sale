import {
    fetchItems,
    imagePreview,
    loadRecord,
    setSelectOptions,
    setValue,
    showNotFound,
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
        showNotFound(main)
        return
    }

    document.getElementById("productTemplateId").value = productTemplate.id
    setValue("name", productTemplate.name)
    setValue("code", productTemplate.code)
    setSelectOptions("category_name", categories, productTemplate.category_id, "Select category")
    setSelectOptions("sub_category_name", subCategories, productTemplate.sub_category_id, "Select sub category")
    setSelectOptions("brand_name", brands, productTemplate.brand_id, "Select brand")
    setValue("mrp", productTemplate.mrp)
    setValue("tax", productTemplate.tax)
    setValue("description", productTemplate.description)
    setValue("openstock", productTemplate.openstock)
    imagePreview("imagePreview", productTemplate.image)

    const form = document.getElementById("submitForm")

    form.addEventListener("submit", (event) => {
        event.preventDefault()
        updateRecord("product_template", id, form, "#/product_template")
    })
}
