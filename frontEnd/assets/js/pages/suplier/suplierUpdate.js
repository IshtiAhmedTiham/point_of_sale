import {
    fetchItems,
    imagePreview,
    loadRecord,
    setSelectOptions,
    setValue,
    showNotFound,
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
        showNotFound(main)
        return
    }

    document.getElementById("suplierId").value = suplier.id
    setValue("name", suplier.name)
    setSelectOptions("brand_name", brands, suplier.brand_id, "Select brand")
    setValue("phone", suplier.phone)
    setValue("address", suplier.address)
    setValue("account_no", suplier.account_no)
    setValue("opening_balance", suplier.opening_balance)
    imagePreview("imagePreview", suplier.image)

    const form = document.getElementById("submitForm")

    form.addEventListener("submit", (event) => {
        event.preventDefault()
        updateRecord("suplier", id, form, "#/suplier")
    })
}
