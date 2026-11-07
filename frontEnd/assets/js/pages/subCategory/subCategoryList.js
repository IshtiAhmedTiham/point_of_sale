import { attachDelete, imageCell, loadRecord, fetchItems} from "../../utils/helpers.js"

export async function subCategoryPage() {
    const main = document.getElementById("main-content")

    const subCategoryContent = await fetch("pages/subCategory/read.html")
    main.innerHTML = await subCategoryContent.text()


    async function render() {
        const tbody = document.getElementById("tbody")
        const items = await fetchItems("subcategory")

        if (!items.length) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="8">
                        <div class="empty-state">
                            <i class="fas fa-sitemap"></i>
                            <strong>No sub categories yet</strong>
                            <span>Create a sub category to keep product families organized.</span>
                        </div>
                    </td>
                </tr>
            `
        }


        let sl = 1;

        const rows = await Promise.all(
            items.map(async (value) => {
                const statusClass = value.status == "Active" ? "status-active" : "status-inactive"
                const image = imageCell(value.icon)

                const category = await loadRecord("category", value.category_id)

                return `
                    <tr>
                        <td>${sl++}</td>
                        <td>${image}</td>
                        <td><strong>${value.name}</strong></td>
                        <td><span class="payment-pill">${category?.name ?? "-"}</span></td>
                        <td>${value.code}</td>
                        <td>${value.description ?? "-"}</td>
                        <td><span class="status-badge ${statusClass}">${value.status}</span></td>
                        <td class="text-center">
                            <a
                                class="btn table-action table-action-edit"
                                href="#/subcategory/update?id=${value.id}"
                                title="Edit"
                            >
                                <i class="fas fa-edit"></i>
                            </a>

                            <button
                                class="btn table-action table-action-delete"
                                data-delete="${value.id}"
                                title="Delete"
                            >
                                <i class="fas fa-trash"></i>
                            </button>

                        </td>

                    </tr>
                `
            })

        )

        tbody.innerHTML = rows.join("")

        attachDelete(tbody, "subcategory", render)
    }
    
    render()
}