const API_BASE = "http://127.0.0.1:8000/api/v1"

const endpoints = {
    products: `${API_BASE}/product_template`,
    categories: `${API_BASE}/category/`,
    subcategories: `${API_BASE}/subcategory`,
    brands: `${API_BASE}/brand`,
    customers: `${API_BASE}/customer`,
    suppliers: `${API_BASE}/suplier`,
    users: `${API_BASE}/user`,
    purchases: `${API_BASE}/purchase`
}

function toDate(value) {
    const date = new Date(value)
    return Number.isNaN(date.getTime()) ? null : date
}

function formatNumber(value) {
    return Number(value || 0).toLocaleString(undefined, {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    })
}

function formatCount(value) {
    return Number(value || 0).toLocaleString()
}

function formatCompact(value) {
    if (value >= 1000000) return `${(value / 1000000).toFixed(1)}m`
    if (value >= 1000) return `${(value / 1000).toFixed(value >= 10000 ? 0 : 1)}k`
    return `${Math.round(value)}`
}

function pageTotal(data) {
    if (!data) return 0
    if (typeof data.total === "number") return data.total
    return Array.isArray(data.items) ? data.items.length : 0
}

function purchaseAmount(purchase) {
    return Number(
        purchase?.purchase_billing?.net_total
        ?? purchase?.net_total
        ?? (Number(purchase?.unit_cost || 0) * Number(purchase?.quantity || 0))
    ) || 0
}

async function fetchEndpoint(url) {
    const response = await fetch(url)
    if (!response.ok) throw new Error(`Request failed: ${url}`)
    return response.json()
}

function smoothPath(points) {
    if (!points.length) return ""
    if (points.length === 1) return `M ${points[0].x} ${points[0].y}`

    let path = `M ${points[0].x} ${points[0].y}`

    for (let index = 1; index < points.length; index++) {
        const previous = points[index - 1]
        const current = points[index]
        const controlX = (previous.x + current.x) / 2
        path += ` C ${controlX} ${previous.y}, ${controlX} ${current.y}, ${current.x} ${current.y}`
    }

    return path
}

function buildPurchaseSeries(purchases) {
    const items = purchases?.items ?? []
    const grouped = new Map()

    items.forEach((purchase) => {
        const date = toDate(purchase.date)
        if (!date) return

        const key = date.toISOString().slice(0, 10)
        const current = grouped.get(key) ?? { date, value: 0 }
        current.value += purchaseAmount(purchase)
        grouped.set(key, current)
    })

    return Array.from(grouped.values())
        .sort((first, second) => first.date - second.date)
        .slice(-8)
}

function renderKpis(data, failed) {
    const cards = [
        ["kpiProducts", "products"],
        ["kpiCategories", "categories"],
        ["kpiCustomers", "customers"],
        ["kpiSuppliers", "suppliers"]
    ]

    cards.forEach(([elementId, key]) => {
        const element = document.getElementById(elementId)
        if (!element) return
        element.textContent = failed.has(key) ? "—" : formatCount(pageTotal(data[key]))
    })
}

function renderChart(purchases) {
    const container = document.getElementById("purchaseChart")
    const totalElement = document.getElementById("chartTotal")
    const noteElement = document.getElementById("chartNote")
    if (!container) return

    const series = buildPurchaseSeries(purchases)
    const total = series.reduce((sum, point) => sum + point.value, 0)

    if (totalElement) totalElement.textContent = formatNumber(total)

    if (!series.length) {
        container.innerHTML = `
            <div class="empty-state dashboard-empty">
                <i class="fas fa-chart-area"></i>
                <strong>No purchases yet</strong>
                <span>New purchase records will appear here automatically.</span>
            </div>
        `
        if (noteElement) noteElement.textContent = "Purchase activity is waiting for its first record."
        return
    }

    const width = 640
    const height = 250
    const padding = { top: 20, right: 18, bottom: 36, left: 54 }
    const plotWidth = width - padding.left - padding.right
    const plotHeight = height - padding.top - padding.bottom
    const baseline = padding.top + plotHeight
    const maxValue = Math.max(...series.map((point) => point.value), 1)

    const xAt = (index) => {
        if (series.length === 1) return padding.left + plotWidth / 2
        return padding.left + (plotWidth * index) / (series.length - 1)
    }

    const yAt = (value) => padding.top + plotHeight - (value / maxValue) * plotHeight

    const points = series.map((point, index) => ({
        x: xAt(index),
        y: yAt(point.value),
        value: point.value,
        date: point.date
    }))

    const linePath = smoothPath(points)
    const areaPath = `${linePath} L ${points[points.length - 1].x} ${baseline} L ${points[0].x} ${baseline} Z`

    const gridLines = []
    for (let index = 0; index <= 4; index++) {
        const y = padding.top + (plotHeight / 4) * index
        const labelValue = maxValue - (maxValue / 4) * index
        gridLines.push(`
            <line class="chart-grid-line" x1="${padding.left}" y1="${y}" x2="${width - padding.right}" y2="${y}"></line>
            <text class="chart-axis-label" x="${padding.left - 10}" y="${y + 3}" text-anchor="end">${formatCompact(labelValue)}</text>
        `)
    }

    const dateLabels = points.map((point) => {
        const label = point.date.toLocaleDateString(undefined, { month: "short", day: "numeric" })
        return `<text class="chart-axis-label" x="${point.x}" y="${height - 12}" text-anchor="middle">${label}</text>`
    }).join("")

    const circles = points.map((point) => {
        const label = point.date.toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" })
        return `
            <circle class="chart-point" cx="${point.x}" cy="${point.y}" r="3.5">
                <title>${label}: ${formatNumber(point.value)}</title>
            </circle>
        `
    }).join("")

    container.innerHTML = `
        <svg class="chart-svg" viewBox="0 0 ${width} ${height}" role="img" aria-label="Purchase value trend">
            <defs>
                <linearGradient id="posChartGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stop-color="#4d0caf" stop-opacity=".2"></stop>
                    <stop offset="100%" stop-color="#4d0caf" stop-opacity="0"></stop>
                </linearGradient>
            </defs>
            ${gridLines.join("")}
            <path class="chart-area" d="${areaPath}"></path>
            <path class="chart-line" d="${linePath}"></path>
            ${circles}
            ${dateLabels}
        </svg>
    `

    if (noteElement) {
        const records = purchases?.items?.length ?? 0
        noteElement.textContent = `Showing net purchase value for the latest ${series.length} activity ${series.length === 1 ? "day" : "days"} from ${records} ${records === 1 ? "record" : "records"}.`
    }
}

function renderBreakdown(data) {
    const container = document.getElementById("catalogBreakdown")
    if (!container) return

    const rows = [
        { label: "Products", value: pageTotal(data.products), color: "#4d0caf" },
        { label: "Categories", value: pageTotal(data.categories), color: "#818048" },
        { label: "Sub categories", value: pageTotal(data.subcategories), color: "#141414" },
        { label: "Brands", value: pageTotal(data.brands), color: "#5d7385" },
        { label: "Suppliers", value: pageTotal(data.suppliers), color: "#c4432f" }
    ]

    const maxValue = Math.max(...rows.map((row) => row.value), 1)

    container.innerHTML = rows.map((row) => {
        const width = row.value === 0 ? 0 : Math.max(8, Math.round((row.value / maxValue) * 100))

        return `
            <div class="breakdown-row">
                <div class="breakdown-meta">
                    <span>
                        <i class="breakdown-dot" style="background: ${row.color};"></i>
                        ${row.label}
                    </span>
                    <strong>${formatCount(row.value)}</strong>
                </div>
                <div class="progress">
                    <div class="progress-bar" style="width: ${width}%; background: ${row.color};"></div>
                </div>
            </div>
        `
    }).join("")
}

function renderRecentPurchases(data) {
    const tbody = document.getElementById("recentPurchasesBody")
    if (!tbody) return

    const suppliers = new Map((data.suppliers?.items ?? []).map((item) => [item.id, item.name]))
    const products = new Map((data.products?.items ?? []).map((item) => [item.id, item.name]))

    const purchases = [...(data.purchases?.items ?? [])]
        .sort((first, second) => {
            const firstDate = toDate(first.date)
            const secondDate = toDate(second.date)
            return (secondDate?.getTime() ?? 0) - (firstDate?.getTime() ?? 0)
        })
        .slice(0, 6)

    if (!purchases.length) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5">
                    <div class="empty-state">
                        <i class="fas fa-receipt"></i>
                        <strong>No purchases recorded</strong>
                        <span>Stock received into the store will show up here.</span>
                    </div>
                </td>
            </tr>
        `
        return
    }

    tbody.innerHTML = purchases.map((purchase) => {
        const supplier = suppliers.get(purchase.suplier_id) ?? `Supplier #${purchase.suplier_id}`
        const product = products.get(purchase.product_id) ?? `Product #${purchase.product_id}`
        const payment = purchase.purchase_billing?.payment_method ?? "—"
        const purchaseDate = toDate(purchase.date)

        return `
            <tr>
                <td>${purchaseDate ? purchaseDate.toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" }) : "—"}</td>
                <td><strong>${supplier}</strong></td>
                <td>${product}</td>
                <td><span class="payment-pill">${payment}</span></td>
                <td>${formatNumber(purchaseAmount(purchase))}</td>
            </tr>
        `
    }).join("")
}

async function initDashboard() {
    const dateElement = document.querySelector("#dashboardDate span")
    if (dateElement) {
        dateElement.textContent = new Date().toLocaleDateString(undefined, {
            weekday: "long",
            month: "short",
            day: "numeric",
            year: "numeric"
        })
    }

    const keys = Object.keys(endpoints)
    const results = await Promise.allSettled(keys.map((key) => fetchEndpoint(endpoints[key])))

    const data = {}
    const failed = new Set()

    keys.forEach((key, index) => {
        const result = results[index]
        if (result.status === "fulfilled") {
            data[key] = result.value
        } else {
            failed.add(key)
            data[key] = { items: [], total: 0 }
        }
    })

    if (failed.size) {
        const notice = document.getElementById("dashboardNotice")
        if (notice) notice.hidden = false
    }

    renderKpis(data, failed)
    renderChart(data.purchases)
    renderBreakdown(data)
    renderRecentPurchases(data)
}

export async function dashboardContent() {
    const mainContent = document.getElementById("main-content")
    const response = await fetch("pages/dashboard.html")
    const htmlContent = await response.text()

    mainContent.innerHTML = htmlContent

    await initDashboard()
}
