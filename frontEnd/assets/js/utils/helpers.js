export const API_BASE = "http://127.0.0.1:8000/api/v1"
export const STATIC_BASE = "http://127.0.0.1:5500"

export function imageCell(path) {
    if (!path) return `<span class="text-muted">—</span>`

    const source = `${STATIC_BASE}/${path}`
    
    return `<img class="table-thumb" src="${source}">`
}


export async function fetchItems(section) {
    const response = await fetch(`${API_BASE}/${section}`)

    const data = await response.json()
    return data.items ?? []
}


export async function loadRecord(section, id) {
    const items = await fetchItems(section)
    
    return items.find((item) => item.id == id)
}


export async function updateRecord(section, id, form) {
    const response = await fetch(`${API_BASE}/${section}/${id}`, {
        method: "PUT",
        body: new FormData(form)
    })

    if (response.ok){
        window.location.hash = `/${section}`
    }else{
        alert("Data Successfully Updated")
    }
}


export function attachDelete(tbody, section, render) {
    tbody.addEventListener("click", async (event) => {

        const button = event.target.closest("[data-delete]")

        const id = button.dataset.delete;

        const response = await fetch(`${API_BASE}/${section}/${id}`, {
            method: "DELETE"
        })

        if (response.ok) {
            alert("Data Deleted Successfully")
            render()
        } else {
            alert("Data Delete Successfully Failed")
        }
    })
}

