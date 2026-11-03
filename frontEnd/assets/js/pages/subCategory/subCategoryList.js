function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>"']/g, (char) => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;"
    }[char]))
}

export async function subCategoryPage() {
    const main = document.getElementById("main-content")

    async function render() {
        const subCategoryContent = await fetch("pages/subCategory/read.html")
        main.innerHTML = await subCategoryContent.text()

        const tbody = document.getElementById("tbody")
        const content = await fetch("http://127.0.0.1:8000/api/v1/subcategory/")
        const data = await content.json()
        const items = data.items ?? []

        if (!items.length) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="8">
                        <div class="empty-state">
                            <i class="fas fa-sitemap"></i>
                            <strong>No sub categories yet</strong>
                            <span>Create a sub category to keep product families organized.</span>
                        </div>
                    </td>
                </tr>
            `
            return
        }

        let sl = 1

        tbody.innerHTML = items.map(value => {
            const status = escapeHtml(value.status)
            const statusClass = value.status === "Active" ? "status-active" : "status-inactive"
            const image = value.icon
                ? `<img class="table-thumb" src="http://127.0.0.1:5500/${escapeHtml(value.icon)}" alt="${escapeHtml(value.name)}">`
                : `<span class="text-muted">—</span>`

            return `
                <tr>
                    <td>${sl++}</td>
                    <td>${image}</td>
                    <td><strong>${escapeHtml(value.name)}</strong></td>
                    <td><span class="payment-pill">#${escapeHtml(value.category_id)}</span></td>
                    <td>${escapeHtml(value.code)}</td>
                    <td>${escapeHtml(value.description)}</td>
                    <td><span class="status-badge ${statusClass}">${status}</span></td>
                    <td class="text-center">
                        <a class="btn table-action table-action-edit" href="#/subcategory/update?id=${value.id}" title="Edit">
                            <i class="fas fa-edit"></i>
                        </a>
                        <button class="btn table-action table-action-delete" data-id="${value.id}" title="Delete">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `
        }).join("")

        tbody.addEventListener("click", async (event) => {
            const btn = event.target.closest("[data-id]")
            if (!btn) return

            const id = btn.dataset.id

            await fetch(`http://127.0.0.1:8000/api/v1/subcategory/${id}`, {
                method: "DELETE",
                body: ""
            })

            alert("Data Successfully Deleted")
            render()
        })
    }

    render()
}
