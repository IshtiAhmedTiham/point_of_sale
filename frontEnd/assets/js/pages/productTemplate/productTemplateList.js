import {
    attachDelete,
    buildNameMap,
    emptyRow,
    escapeHtml,
    fetchItems,
    formatMoney,
    imageCell,
    nameFromMap
} from "../../utils/helpers.js"

export async function productTemplatePage() {
    const main = document.getElementById("main-content")
    const response = await fetch("pages/productTemplate/read.html")

    main.innerHTML = await response.text()

    const tbody = document.getElementById("tbody")

    attachDelete(tbody, "product_template", render)

    async function render() {
        const [items, categories, subCategories, brands] = await Promise.all([
            fetchItems("product_template"),
            fetchItems("category"),
            fetchItems("subcategory"),
            fetchItems("brand")
        ])

        if (!items.length) {
            tbody.innerHTML = emptyRow(
                12,
                "fa-boxes",
                "No product templates yet",
                "Product templates added to the catalog will appear here."
            )
            return
        }

        const categoriesById = buildNameMap(categories)
        const subCategoriesById = buildNameMap(subCategories)
        const brandsById = buildNameMap(brands)
        let serial = 1

        tbody.innerHTML = items.map((item) => `
            <tr>
                <td>${serial++}</td>
                <td>${imageCell(item.image, item.name)}</td>
                <td><strong>${escapeHtml(item.name)}</strong></td>
                <td>${escapeHtml(item.code)}</td>
                <td>${escapeHtml(nameFromMap(categoriesById, item.category_id, "Category"))}</td>
                <td>${escapeHtml(nameFromMap(subCategoriesById, item.sub_category_id, "Sub category"))}</td>
                <td>${escapeHtml(nameFromMap(brandsById, item.brand_id, "Brand"))}</td>
                <td>${formatMoney(item.mrp)}</td>
                <td>${formatMoney(item.tax)}</td>
                <td>${escapeHtml(item.description)}</td>
                <td>${escapeHtml(item.openstock)}</td>
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
    }

    render()
}
