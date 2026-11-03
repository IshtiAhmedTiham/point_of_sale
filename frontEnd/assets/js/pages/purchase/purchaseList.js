import {
    attachDelete,
    buildNameMap,
    emptyRow,
    escapeHtml,
    fetchItems,
    formatDate,
    formatMoney,
    nameFromMap
} from "../../utils/helpers.js"

export async function purchasePage() {
    const main = document.getElementById("main-content")
    const response = await fetch("pages/purchase/read.html")

    main.innerHTML = await response.text()

    const tbody = document.getElementById("tbody")

    attachDelete(tbody, "purchase", render)

    async function render() {
        const [items, suppliers, products, brands] = await Promise.all([
            fetchItems("purchase"),
            fetchItems("suplier"),
            fetchItems("product_template"),
            fetchItems("brand")
        ])

        if (!items.length) {
            tbody.innerHTML = emptyRow(
                12,
                "fa-cart-plus",
                "No purchases yet",
                "Stock purchases recorded in the store will appear here."
            )
            return
        }

        const suppliersById = buildNameMap(suppliers)
        const productsById = buildNameMap(products)
        const brandsById = buildNameMap(brands)
        let serial = 1

        tbody.innerHTML = items.map((item) => {
            const billing = item.purchase_billing ?? {}

            return `
                <tr>
                    <td>${serial++}</td>
                    <td>${formatDate(item.date)}</td>
                    <td>${escapeHtml(nameFromMap(suppliersById, item.suplier_id, "Supplier"))}</td>
                    <td>${escapeHtml(nameFromMap(productsById, item.product_id, "Product"))}</td>
                    <td>${escapeHtml(nameFromMap(brandsById, item.brand_id, "Brand"))}</td>
                    <td>${formatMoney(item.unit_cost)}</td>
                    <td>${escapeHtml(item.quantity)}</td>
                    <td>${formatMoney(item.tax)}</td>
                    <td>${formatMoney(item.sub_total)}</td>
                    <td><span class="payment-pill">${escapeHtml(billing.payment_method || "—")}</span></td>
                    <td>${formatMoney(billing.net_total)}</td>
                    <td class="text-center">
                        <a class="btn table-action table-action-edit" href="#/purchase/update?id=${item.id}" title="Edit">
                            <i class="fas fa-edit"></i>
                        </a>
                        <button class="btn table-action table-action-delete" data-delete="${item.id}" title="Delete">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `
        }).join("")
    }

    render()
}
