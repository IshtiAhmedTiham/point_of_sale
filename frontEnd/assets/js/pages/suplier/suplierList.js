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
            tbody.innerHTML = emptyRow(
                9,
                "fa-truck",
                "No suppliers yet",
                "Supplier partners added to the store will appear here."
            )
            return
        }

        const brandsById = buildNameMap(brands)
        let serial = 1

        tbody.innerHTML = items.map((item) => `
            <tr>
                <td>${serial++}</td>
                <td>${imageCell(item.image, item.name)}</td>
                <td><strong>${escapeHtml(item.name)}</strong></td>
                <td>${escapeHtml(nameFromMap(brandsById, item.brand_id, "Brand"))}</td>
                <td>${escapeHtml(item.phone)}</td>
                <td>${escapeHtml(item.address)}</td>
                <td>${escapeHtml(item.account_no)}</td>
                <td>${formatMoney(item.opening_balance)}</td>
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
    }

    render()
}
