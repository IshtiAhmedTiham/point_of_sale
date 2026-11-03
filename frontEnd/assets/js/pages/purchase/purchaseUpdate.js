import {
    fetchItems,
    loadRecord,
    setSelectOptions,
    setValue,
    showNotFound,
    toDateTimeLocal,
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
        showNotFound(main)
        return
    }

    const billing = purchase.purchase_billing ?? {}

    document.getElementById("purchaseId").value = purchase.id
    setValue("date", toDateTimeLocal(purchase.date))
    setSelectOptions("suplier_name", suppliers, purchase.suplier_id, "Select supplier")
    setSelectOptions("product_name", products, purchase.product_id, "Select product")
    setSelectOptions("brand_name", brands, purchase.brand_id, "Select brand")
    setValue("unit_cost", purchase.unit_cost)
    setValue("quantity", purchase.quantity)
    setValue("tax", purchase.tax)
    setValue("sub_total", purchase.sub_total)
    setValue("total", billing.total)
    setValue("discount", billing.discount)
    setValue("net_total", billing.net_total)
    setValue("payment_method", billing.payment_method)
    setValue("pay", billing.pay)
    setValue("due", billing.due)

    const form = document.getElementById("submitForm")

    form.addEventListener("submit", (event) => {
        event.preventDefault()
        updateRecord("purchase", id, form, "#/purchase")
    })
}
