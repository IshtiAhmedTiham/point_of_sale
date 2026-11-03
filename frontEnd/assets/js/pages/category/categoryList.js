export async function categoryPage() {
    const main = document.getElementById("main-content")

    async function render() {
        const categoryContent = await fetch("pages/category/read.html")
        main.innerHTML = await categoryContent.text()

        const tbody = document.getElementById("tbody")
        const response = await fetch("http://127.0.0.1:8000/api/v1/category/")
        const data = await response.json()
        const items = data.items ?? []

        if (!items.length) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7">
                        <div class="empty-state">
                            <i class="fas fa-layer-group"></i>
                            <strong>No categories yet</strong>
                            <span>Add your first category to start building the catalog.</span>
                        </div>
                    </td>
                </tr>
            `
            return
        }

        let sl = 1

        tbody.innerHTML = items.map(value => {
            const statusClass = value.status === "Active" ? "status-active" : "status-inactive"
            const image = value.icon
                ? `<img class="table-thumb" src="http://127.0.0.1:5500/${value.icon}" alt="${value.name}">`
                : `<span class="text-muted">—</span>`

            return `
                <tr>
                    <td>${sl++}</td>
                    <td>${image}</td>
                    <td><strong>${value.name}</strong></td>
                    <td>${value.code}</td>
                    <td>${value.description}</td>
                    <td><span class="status-badge ${statusClass}">${value.status}</span></td>
                    <td class="text-center">
                        <a class="btn table-action table-action-edit" href="#/category/update?id=${value.id}" title="Edit">
                            <i class="fas fa-edit"></i>
                        </a>
                        <button class="btn table-action table-action-delete" data-delete="${value.id}" title="Delete">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `
        }).join("")

        tbody.addEventListener("click", async (event) => {
            const btn = event.target.closest("[data-delete]")
            if (!btn) return

            const id = btn.dataset.delete

            await fetch(`http://127.0.0.1:8000/api/v1/category/${id}`, {
                method: "DELETE",
                body: ""
            })

            alert("Data Successfully Deleted")
            render()
        })
    }

    render()
}
