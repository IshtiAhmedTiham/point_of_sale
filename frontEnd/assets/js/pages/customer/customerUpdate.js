import {
    imagePreview,
    loadRecord,
    setValue,
    showNotFound,
    updateRecord
} from "../../utils/helpers.js"

export async function customerUpdatePage(params) {
    const id = params.get("id")
    const main = document.getElementById("main-content")
    const response = await fetch("pages/customer/update.html")

    main.innerHTML = await response.text()

    const customer = await loadRecord("customer", id)

    if (!customer) {
        showNotFound(main)
        return
    }

    document.getElementById("customerId").value = customer.id
    setValue("name", customer.name)
    setValue("email", customer.email)
    setValue("phone", customer.phone)
    setValue("address", customer.address)
    setValue("account_no", customer.account_no)
    setValue("opening_balance", customer.opening_balance)
    setValue("discount", customer.discount)
    setValue("taxable", customer.taxable)
    imagePreview("imagePreview", customer.icon)

    const form = document.getElementById("submitForm")

    form.addEventListener("submit", (event) => {
        event.preventDefault()
        updateRecord("customer", id, form, "#/customer")
    })
}
