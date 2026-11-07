import {
    attachDelete,
    fetchItems
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
            main.innerHTML = "<p>Category not found.</p>"
            return
        }

        let serial = 1

        tbody.innerHTML = items.map((item) => {
            const billing = item.purchase_billing ?? {}

            return `
                <tr>
                    <td>${serial++}</td>
                    <td>${Number.isNaN(new Date(item.date).getTime()) ? "—" : new Date(item.date).toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" })}</td>
                    <td>${item.suplier_id ? (suppliers.find((supplier) => supplier.id === item.suplier_id)?.name ?? `Supplier #${item.suplier_id}`) : "—"}</td>
                    <td>${item.product_id ? (products.find((product) => product.id === item.product_id)?.name ?? `Product #${item.product_id}`) : "—"}</td>
                    <td>${item.brand_id ? (brands.find((brand) => brand.id === item.brand_id)?.name ?? `Brand #${item.brand_id}`) : "—"}</td>
                    <td>${(item.unit_cost||0).toFixed(2)}</td>
                    <td>${item.quantity}</td>
                    <td>${(item.tax||0).toFixed(2)}</td>
                    <td>${(item.sub_total||0).toFixed(2)}</td>
                    <td><span class="payment-pill">${billing.payment_method || "—"}</span></td>
                    <td>${(billing.net_total||0).toFixed(2)}</td>
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

        attachDelete(tbody, "purchase", render, "purchase")

    }

    render()
}
