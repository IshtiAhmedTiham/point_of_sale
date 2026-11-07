import {
    loadRecord,
    updateRecord
} from "../../utils/helpers.js"

export async function customerUpdatePage(params) {
    const id = params.get("id")
    const main = document.getElementById("main-content")
    const response = await fetch("pages/customer/update.html")

    main.innerHTML = await response.text()

    const customer = await loadRecord("customer", id)

    if (!customer) {
        main.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-exclamation-circle"></i>
                <strong>Record not found</strong>
                <span>The requested record could not be found.</span>
            </div>
        `
        return
    }

    document.getElementById("customerId").value = customer.id
    document.getElementById("name").value = customer.name ?? ""
    document.getElementById("email").value = customer.email ?? ""
    document.getElementById("phone").value = customer.phone ?? ""
    document.getElementById("address").value = customer.address ?? ""
    document.getElementById("account_no").value = customer.account_no ?? ""
    document.getElementById("opening_balance").value = customer.opening_balance ?? ""
    document.getElementById("discount").value = customer.discount ?? ""
    document.getElementById("taxable").value = customer.taxable ?? ""
    document.getElementById("imagePreview").src = `http://127.0.0.1:5500/${customer.icon}`

    const form = document.getElementById("submitForm")

    form.addEventListener("submit", (event) => {
        event.preventDefault()
        updateRecord("customer", id, form, "#/customer")
    })
}
