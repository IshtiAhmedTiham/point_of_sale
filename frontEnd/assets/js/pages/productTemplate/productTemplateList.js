import {
    attachDelete,
    fetchItems,
    imageCell
} from "../../utils/helpers.js"

export async function productTemplatePage() {
    const main = document.getElementById("main-content")
    const response = await fetch("pages/productTemplate/read.html")

    main.innerHTML = await response.text()

    const tbody = document.getElementById("tbody")

    
    async function render() {
        const [items, categories, subCategories, brands] = await Promise.all([
            fetchItems("product_template"),
            fetchItems("category"),
            fetchItems("subcategory"),
            fetchItems("brand")
        ])
        
        if (!items.length) {
            main.innerHTML = "<p>Category not found.</p>"
            return
        }

        let serial = 1


        tbody.innerHTML = items.map((item) => `
            <tr>
                <td>${serial++}</td>
                <td>${imageCell(item.image, item.name)}</td>
                <td><strong>${item.name}</strong></td>
                <td>${item.code}</td>
                <td>${item.category_id ? (categories.find((category) => category.id === item.category_id)?.name ?? `Category #${item.category_id}`) : "—"}</td>
                <td>${item.sub_category_id ? (subCategories.find((subCategory) => subCategory.id === item.sub_category_id)?.name ?? `Sub category #${item.sub_category_id}`) : "—"}</td>
                <td>${item.brand_id ? (brands.find((brand) => brand.id === item.brand_id)?.name ?? `Brand #${item.brand_id}`) : "—"}</td>
                <td>${(item.mrp||0).toFixed(2)}</td>
                <td>${(item.tax||0).toFixed(2)}</td>
                <td>${item.description}</td>
                <td>${item.openstock}</td>
                <td class="text-center">
                    <a class="btn table-action table-action-edit" href="#/product_template/update?id=${item.id}" title="Edit">
                        <i class="fas fa-edit"></i>
                    </a>
                    <button class="btn table-action table-action-delete" data-delete="${item.id}" title="Delete">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
        `).join("")
        
        attachDelete(tbody, "product_template", render, "product_template")
    }

    render()
}
