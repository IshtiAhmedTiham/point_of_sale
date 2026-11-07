import {
    fetchItems,
    loadRecord,
    updateRecord
} from "../../utils/helpers.js"

export async function purchaseUpdatePage(params) {
    const id = params.get("id")
    const main = document.getElementById("main-content")
    const response = await fetch("pages/purchase/update.html")

    main.innerHTML = await response.text()

    const [purchase, suppliers, products, brands] = await Promise.all([
        loadRecord("purchase", id),
        fetchItems("suplier"),
        fetchItems("product_template"),
        fetchItems("brand")
    ])

    if (!purchase) {
        main.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-exclamation-circle"></i>
                <strong>Record not found</strong>
                <span>The requested record could not be found.</span>
            </div>
        `
        return
    }

    const billing = purchase.purchase_billing ?? {}

    document.getElementById("purchaseId").value = purchase.id
    const purchaseDate = new Date(purchase.date)
    const pad = (part) => String(part).padStart(2, "0")
    document.getElementById("date").value = Number.isNaN(purchaseDate.getTime()) ? "" : `${purchaseDate.getFullYear()}-${pad(purchaseDate.getMonth() + 1)}-${pad(purchaseDate.getDate())}T${pad(purchaseDate.getHours())}:${pad(purchaseDate.getMinutes())}`
    const supplierSelect = document.getElementById("suplier_name")
    supplierSelect.innerHTML = `<option value="">Select supplier</option>` + suppliers.map((supplier) => `
        <option value="${supplier.name}" ${String(supplier.id) === String(purchase.suplier_id) ? "selected" : ""}>
            ${supplier.name}
        </option>
    `).join("")
    const productSelect = document.getElementById("product_name")
    productSelect.innerHTML = `<option value="">Select product</option>` + products.map((product) => `
        <option value="${product.name}" ${String(product.id) === String(purchase.product_id) ? "selected" : ""}>
            ${product.name}
        </option>
    `).join("")
    const brandSelect = document.getElementById("brand_name")
    brandSelect.innerHTML = `<option value="">Select brand</option>` + brands.map((brand) => `
        <option value="${brand.name}" ${String(brand.id) === String(purchase.brand_id) ? "selected" : ""}>
            ${brand.name}
        </option>
    `).join("")
    document.getElementById("unit_cost").value = purchase.unit_cost ?? ""
    document.getElementById("quantity").value = purchase.quantity ?? ""
    document.getElementById("tax").value = purchase.tax ?? ""
    document.getElementById("sub_total").value = purchase.sub_total ?? ""
    document.getElementById("total").value = billing.total ?? ""
    document.getElementById("discount").value = billing.discount ?? ""
    document.getElementById("net_total").value = billing.net_total ?? ""
    document.getElementById("payment_method").value = billing.payment_method ?? ""
    document.getElementById("pay").value = billing.pay ?? ""
    document.getElementById("due").value = billing.due ?? ""

    const form = document.getElementById("submitForm")

    form.addEventListener("submit", (event) => {
        event.preventDefault()
        updateRecord("purchase", id, form, "#/purchase")
    })
}
