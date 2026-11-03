import { sidebar } from "./components/sidebar.js"
import { topbar } from "./components/topbar.js"
import { initRouter } from "./router.js"

await sidebar()
await topbar()
initRouter()