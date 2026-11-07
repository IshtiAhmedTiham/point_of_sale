import { attachDelete, imageCell, fetchItems} from "../../utils/helpers.js"

export async function categoryPage() {
    const main = document.getElementById("main-content")

    const categoryContent = await fetch("pages/category/read.html")
    main.innerHTML = await categoryContent.text()

    const tbody = document.getElementById("tbody")

    async function render() {
        const items = await fetchItems("category")

        if (!items.length) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7">
                        <div class="empty-state">
                            <i class="fas fa-layer-group"></i>
                            <strong>No categories yet</strong>
                            <span>Add your first category to start building the catalog.</span>
                        </div>
                    </td>
                </tr>
            `
            return
        }

        let sl = 1

        tbody.innerHTML = items.map(value => {
            const statusClass = value.status === "Active" ? "status-active" : "status-inactive"
            const image = imageCell(value.icon)

            return `
                <tr>
                    <td>${sl++}</td>
                    <td>${image}</td>
                    <td><strong>${value.name}</strong></td>
                    <td>${value.code}</td>
                    <td>${value.description}</td>
                    <td>
                        <span class="status-badge ${statusClass}">
                            ${value.status}
                        </span>
                    </td>
                    <td class="text-center">
                        <a class="btn table-action table-action-edit"
                           href="#/category/update?id=${value.id}">
                            <i class="fas fa-edit"></i>
                        </a>

                        <button
                            class="btn table-action table-action-delete"
                            data-delete="${value.id}">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `
        }).join("")

        attachDelete(tbody, "category", render)
    }

    render()
}