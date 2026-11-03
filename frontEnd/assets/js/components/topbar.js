export async function topbar(){
    let containerId = document.getElementById("topbar-container")
    let response = await fetch("components/topbar.html")
    
    containerId.innerHTML = await response.text()
}
