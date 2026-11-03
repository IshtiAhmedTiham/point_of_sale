import {
    attachDelete,
    emptyRow,
    escapeHtml,
    fetchItems,
    imageCell,
    statusBadge
} from "../../utils/helpers.js"

export async function brandPage() {
    const main = document.getElementById("main-content")
    const response = await fetch("pages/brand/read.html")

    main.innerHTML = await response.text()

    const tbody = document.getElementById("tbody")

    attachDelete(tbody, "brand", render)

    async function render() {
        const items = await fetchItems("brand")

        if (!items.length) {
            tbody.innerHTML = emptyRow(
                8,
                "fa-tags",
                "No brands yet",
                "Brands added to the catalog will appear here."
            )
            return
        }

        let serial = 1

        tbody.innerHTML = items.map((item) => `
            <tr>
                <td>${serial++}</td>
                <td>${imageCell(item.logo, item.name)}</td>
                <td><strong>${escapeHtml(item.name)}</strong></td>
                <td>${escapeHtml(item.email)}</td>
                <td>${escapeHtml(item.phone)}</td>
                <td>${escapeHtml(item.address)}</td>
                <td>${statusBadge(item.status)}</td>
                <td class="text-center">
                    <a class="btn table-action table-action-edit" href="#/brand/update?id=${item.id}" title="Edit">
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
