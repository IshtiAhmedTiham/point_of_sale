import {
    attachDelete,
    fetchItems,
    imageCell
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
            tbody.innerHTML = `
                <tr>
                    <td colspan="10">
                        <div class="empty-state">
                            <i class="fas fa-user-shield"></i>
                            <strong>No users yet</strong>
                            <span>User accounts added to the store will appear here.</span>
                        </div>
                    </td>
                </tr>
            `
            return
        }

        let serial = 1

        tbody.innerHTML = items.map((item) => `
            <tr>
                <td>${serial++}</td>
                <td>${imageCell(item.image, item.name)}</td>
                <td><strong>${item.name}</strong></td>
                <td>${item.email}</td>
                <td>${item.role}</td>
                <td>${item.branch}</td>
                <td>${item.phone}</td>
                <td>${item.address}</td>
                <td>${item.status}</td>
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

        attachDelete(tbody, "user", render, "user")

    }

    render()
}
