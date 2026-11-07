import {attachDelete, fetchItems, imageCell} from "../../utils/helpers.js"

export async function brandPage() {
    const main = document.getElementById("main-content")
    
    const response = await fetch("pages/brand/read.html")
    main.innerHTML = await response.text()

    const tbody = document.getElementById("tbody")

    async function render() {
        const items = await fetchItems("brand")

        let serial = 1

        tbody.innerHTML = items.map((item) => `
            <tr>
                <td>${serial++}</td>
                <td>${imageCell(item.logo)}</td>
                <td><strong>${item.name}</strong></td>
                <td>${item.email}</td>
                <td>${item.phone}</td>
                <td>${item.address}</td>
                <td>${item.status}</td>
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

        attachDelete(tbody, "brand", render, "brand")

    }

    render()
}
