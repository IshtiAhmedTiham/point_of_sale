import {
    attachDelete,
    emptyRow,
    escapeHtml,
    fetchItems,
    formatMoney,
    imageCell
} from "../../utils/helpers.js"

export async function customerPage() {
    const main = document.getElementById("main-content")
    const response = await fetch("pages/customer/read.html")

    main.innerHTML = await response.text()

    const tbody = document.getElementById("tbody")

    attachDelete(tbody, "customer", render)

    async function render() {
        const items = await fetchItems("customer")

        if (!items.length) {
            tbody.innerHTML = emptyRow(
                11,
                "fa-user-friends",
                "No customers yet",
                "Customer profiles added to the store will appear here."
            )
            return
        }

        let serial = 1

        tbody.innerHTML = items.map((item) => `
            <tr>
                <td>${serial++}</td>
                <td>${imageCell(item.icon, item.name)}</td>
                <td><strong>${escapeHtml(item.name)}</strong></td>
                <td>${escapeHtml(item.email)}</td>
                <td>${escapeHtml(item.phone)}</td>
                <td>${escapeHtml(item.address)}</td>
                <td>${escapeHtml(item.account_no)}</td>
                <td>${formatMoney(item.opening_balance)}</td>
                <td>${formatMoney(item.discount)}</td>
                <td>${formatMoney(item.taxable)}</td>
                <td class="text-center">
                    <a class="btn table-action table-action-edit" href="#/customer/update?id=${item.id}" title="Edit">
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
