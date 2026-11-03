import { dashboardContent } from "./pages/dashboard.js"
import { categoryUpdatePage } from "./pages/category/categoryUpdate.js"
import { subCategoryUpdatePage } from "./pages/subCategory/subCategoryUpdate.js"
import { brandUpdatePage } from "./pages/brand/brandUpdate.js"
import { customerUpdatePage } from "./pages/customer/customerUpdate.js"
import { userUpdatePage } from "./pages/user/userUpdate.js"
import { suplierUpdatePage } from "./pages/suplier/suplierUpdate.js"
import { purchaseUpdatePage } from "./pages/purchase/purchaseUpdate.js"
import { productTemplateUpdatePage } from "./pages/productTemplate/productTemplateUpdate.js"
import { routes } from "./routes.js"

const updateRoutes = [
    { prefix: "#/category/update", page: categoryUpdatePage },
    { prefix: "#/subcategory/update", page: subCategoryUpdatePage },
    { prefix: "#/brand/update", page: brandUpdatePage },
    { prefix: "#/customer/update", page: customerUpdatePage },
    { prefix: "#/user/update", page: userUpdatePage },
    { prefix: "#/suplier/update", page: suplierUpdatePage },
    { prefix: "#/purchase/update", page: purchaseUpdatePage },
    { prefix: "#/product_template/update", page: productTemplateUpdatePage }
]

export function initRouter() {
    function render() {
        const hash = window.location.hash || "#/"

        const updateRoute = updateRoutes.find(({ prefix }) => hash.startsWith(prefix))

        if (updateRoute) {
            const params = new URLSearchParams(hash.split("?")[1] ?? "")
            return updateRoute.page(params)
        }

        const page = routes[hash] || dashboardContent
        page()
    }

    window.addEventListener("hashchange", render)
    render()
}
