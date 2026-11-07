import {
    fetchItems,
    loadRecord,
    updateRecord
} from "../../utils/helpers.js"

export async function suplierUpdatePage(params) {
    const id = params.get("id")
    const main = document.getElementById("main-content")
    const response = await fetch("pages/suplier/update.html")

    main.innerHTML = await response.text()

    const [suplier, brands] = await Promise.all([
        loadRecord("suplier", id),
        fetchItems("brand")
    ])

    if (!suplier) {
        main.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-exclamation-circle"></i>
                <strong>Record not found</strong>
                <span>The requested record could not be found.</span>
            </div>
        `
        return
    }

    document.getElementById("suplierId").value = suplier.id
    document.getElementById("name").value = suplier.name ?? ""
    const brandSelect = document.getElementById("brand_name")
    brandSelect.innerHTML = `<option value="">Select brand</option>` + brands.map((brand) => `
        <option value="${brand.name}" ${String(brand.id) === String(suplier.brand_id) ? "selected" : ""}>
            ${brand.name}
        </option>
    `).join("")
    document.getElementById("phone").value = suplier.phone ?? ""
    document.getElementById("address").value = suplier.address ?? ""
    document.getElementById("account_no").value = suplier.account_no ?? ""
    document.getElementById("opening_balance").value = suplier.opening_balance ?? ""
    document.getElementById("imagePreview").src = `http://127.0.0.1:5500/${suplier.image}`

    const form = document.getElementById("submitForm")

    form.addEventListener("submit", (event) => {
        event.preventDefault()
        updateRecord("suplier", id, form, "#/suplier")
    })
}
