import {
    attachDelete,
    fetchItems,
    imageCell
} from "../../utils/helpers.js"

export async function suplierPage() {
    const main = document.getElementById("main-content")
    const response = await fetch("pages/suplier/read.html")

    main.innerHTML = await response.text()

    const tbody = document.getElementById("tbody")

    attachDelete(tbody, "suplier", render)

    async function render() {
        const [items, brands] = await Promise.all([
            fetchItems("suplier"),
            fetchItems("brand")
        ])

        if (!items.length) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="9">
                        <div class="empty-state">
                            <i class="fas fa-truck"></i>
                            <strong>No suppliers yet</strong>
                            <span>Supplier partners added to the store will appear here.</span>
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
                <td>${item.brand_id ? (brands.find((brand) => brand.id === item.brand_id)?.name ?? `Brand #${item.brand_id}`) : "—"}</td>
                <td>${item.phone}</td>
                <td>${item.address}</td>
                <td>${item.account_no}</td>
                <td>${(item.opening_balance||0).toFixed(2)}</td>
                <td class="text-center">
                    <a class="btn table-action table-action-edit" href="#/suplier/update?id=${item.id}" title="Edit">
                        <i class="fas fa-edit"></i>
                    </a>
                    <button class="btn table-action table-action-delete" data-delete="${item.id}" title="Delete">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
        `).join("")

        attachDelete(tbody, "suplier", render, "suplier")

    }

    render()
}
