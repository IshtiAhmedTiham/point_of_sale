import {
    attachDelete,
    fetchItems,
    imageCell
} from "../../utils/helpers.js"

export async function customerPage() {
    const main = document.getElementById("main-content")
    const response = await fetch("pages/customer/read.html")

    main.innerHTML = await response.text()

    const tbody = document.getElementById("tbody")


    async function render() {
        const items = await fetchItems("customer")

        if (!items.length) {
            main.innerHTML = "<p>Category not found.</p>"
            return
        }

        let serial = 1

        tbody.innerHTML = items.map((item) => `
            <tr>
                <td>${serial++}</td>
                <td>${imageCell(item.icon, item.name)}</td>
                <td><strong>${item.name}</strong></td>
                <td>${item.email}</td>
                <td>${item.phone}</td>
                <td>${item.address}</td>
                <td>${item.account_no}</td>
                <td>${(item.opening_balance||0).toFixed(2)}</td>
                <td>${(item.discount||0).toFixed(2)}</td>
                <td>${(item.taxable||0).toFixed(2)}</td>
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

        attachDelete(tbody, "customer", render)
    }

    render()
}
