export const API_BASE = "http://127.0.0.1:8000/api/v1"
export const STATIC_BASE = "http://127.0.0.1:5500"

export function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>"']/g, (char) => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;"
    }[char]))
}

export function imageCell(path, alt) {
    if (!path) return `<span class="text-muted">—</span>`

    const source = /^https?:\/\//.test(path) ? path : `${STATIC_BASE}/${path}`

    return `<img class="table-thumb" src="${escapeHtml(source)}" alt="${escapeHtml(alt)}">`
}

export function statusBadge(status) {
    const statusClass = status === "Active" ? "status-active" : "status-inactive"
    return `<span class="status-badge ${statusClass}">${escapeHtml(status || "—")}</span>`
}

export function formatMoney(value) {
    return Number(value || 0).toLocaleString(undefined, {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    })
}

export function formatDate(value) {
    const date = new Date(value)
    if (Number.isNaN(date.getTime())) return "—"

    return date.toLocaleDateString(undefined, {
        month: "short",
        day: "numeric",
        year: "numeric"
    })
}

export function toDateTimeLocal(value) {
    const date = new Date(value)
    if (Number.isNaN(date.getTime())) return ""

    const pad = (part) => String(part).padStart(2, "0")

    return [
        `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`,
        `${pad(date.getHours())}:${pad(date.getMinutes())}`
    ].join("T")
}

export async function fetchItems(section) {
    const response = await fetch(`${API_BASE}/${section}`)
    if (!response.ok) throw new Error(`Could not load ${section}`)

    const data = await response.json()
    return data.items ?? []
}

export async function loadRecord(section, id) {
    const items = await fetchItems(section)
    return items.find((item) => String(item.id) === String(id))
}

export function buildNameMap(items) {
    return new Map(items.map((item) => [item.id, item.name]))
}

export function nameFromMap(map, id, fallback = "Record") {
    if (id === null || id === undefined || id === "") return "—"
    return map.get(id) ?? `${fallback} #${id}`
}

export function emptyRow(colspan, icon, title, message) {
    return `
        <tr>
            <td colspan="${colspan}">
                <div class="empty-state">
                    <i class="fas ${icon}"></i>
                    <strong>${escapeHtml(title)}</strong>
                    <span>${escapeHtml(message)}</span>
                </div>
            </td>
        </tr>
    `
}

export function showNotFound(main, title = "Record not found", message = "The requested record could not be found.") {
    main.innerHTML = `
        <div class="empty-state">
            <i class="fas fa-exclamation-circle"></i>
            <strong>${escapeHtml(title)}</strong>
            <span>${escapeHtml(message)}</span>
        </div>
    `
}

export function setValue(id, value) {
    const element = document.getElementById(id)
    if (element) element.value = value ?? ""
}

export function setSelectOptions(id, items, selectedId, placeholder = "Select") {
    const select = document.getElementById(id)
    if (!select) return

    select.innerHTML = `<option value="">${escapeHtml(placeholder)}</option>` + items.map((item) => `
        <option value="${escapeHtml(item.name)}" ${String(item.id) === String(selectedId) ? "selected" : ""}>
            ${escapeHtml(item.name)}
        </option>
    `).join("")
}

export function imagePreview(id, path) {
    const element = document.getElementById(id)
    if (!element || !path) return

    const source = /^https?:\/\//.test(path) ? path : `${STATIC_BASE}/${path}`
    element.src = source
}

export function attachDelete(tbody, section, rerender) {
    tbody.addEventListener("click", async (event) => {
        const button = event.target.closest("[data-delete]")
        if (!button) return

        if (!confirm("Delete this record?")) return

        const response = await fetch(`${API_BASE}/${section}/${button.dataset.delete}`, {
            method: "DELETE"
        })

        if (!response.ok) {
            const data = await response.json().catch(() => ({}))
            alert(data.detail ? `Delete failed: ${JSON.stringify(data.detail)}` : "Delete failed")
            return
        }

        alert("Data Successfully Deleted")
        rerender()
    })
}

export async function updateRecord(section, id, form, listRoute) {
    const response = await fetch(`${API_BASE}/${section}/${id}`, {
        method: "PUT",
        body: new FormData(form)
    })

    if (!response.ok) {
        const data = await response.json().catch(() => ({}))
        alert(data.detail ? `Update failed: ${JSON.stringify(data.detail)}` : "Update failed")
        return
    }

    alert("Data Successfully Updated")
    window.location.hash = listRoute
}
