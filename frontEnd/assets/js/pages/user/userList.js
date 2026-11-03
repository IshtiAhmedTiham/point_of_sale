import {
    attachDelete,
    emptyRow,
    escapeHtml,
    fetchItems,
    imageCell,
    statusBadge
} from "../../utils/helpers.js"

export async function userPage() {
    const main = document.getElementById("main-content")
    const response = await fetch("pages/user/read.html")

    main.innerHTML = await response.text()

    const tbody = document.getElementById("tbody")

    attachDelete(tbody, "user", render)

    async function render() {
        const items = await fetchItems("user")

        if (!items.length) {
            tbody.innerHTML = emptyRow(
                10,
                "fa-user-shield",
                "No users yet",
                "User accounts added to the store will appear here."
            )
            return
        }

        let serial = 1

        tbody.innerHTML = items.map((item) => `
            <tr>
                <td>${serial++}</td>
                <td>${imageCell(item.image, item.name)}</td>
                <td><strong>${escapeHtml(item.name)}</strong></td>
                <td>${escapeHtml(item.email)}</td>
                <td>${escapeHtml(item.role)}</td>
                <td>${escapeHtml(item.branch)}</td>
                <td>${escapeHtml(item.phone)}</td>
                <td>${escapeHtml(item.address)}</td>
                <td>${statusBadge(item.status)}</td>
                <td class="text-center">
                    <a class="btn table-action table-action-edit" href="#/user/update?id=${item.id}" title="Edit">
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
