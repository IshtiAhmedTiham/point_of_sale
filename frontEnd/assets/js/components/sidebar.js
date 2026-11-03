function routeSection(hash) {
    const path = (hash || "#/").split("?")[0].replace(/\/$/, "")

    if (!path || path === "#") return "#/"

    const section = path.split("/")[1]
    return section ? `#/${section}` : "#/"
}

export async function sidebar(){
    let containerId = document.getElementById("sidebar-container")
    let response = await fetch("./././components/sidebar.html")

    containerId.innerHTML = await response.text()

    const links = Array.from(containerId.querySelectorAll("[data-route]"))

    function setActive() {
        const activeRoute = routeSection(window.location.hash)

        links.forEach((link) => {
            const item = link.closest(".nav-item")
            if (!item) return

            const isActive = link.dataset.route === activeRoute
            item.classList.toggle("active", isActive)

            if (isActive) {
                link.setAttribute("aria-current", "page")
            } else {
                link.removeAttribute("aria-current")
            }
        })
    }

    window.addEventListener("hashchange", setActive)
    setActive()
}
