import { dashboardContent } from "./pages/dashboard.js"
import { categoryPage } from "./pages/category/categoryList.js"
import { categoryCreatePage } from "./pages/category/categoryCreate.js"
import { subCategoryPage } from "./pages/subCategory/subCategoryList.js"
import { subCategoryCratePage } from "./pages/subCategory/subCategoryCreate.js"
import { brandPage } from "./pages/brand/brandList.js"
import { customerPage } from "./pages/customer/customerList.js"
import { userPage } from "./pages/user/userList.js"
import { suplierPage } from "./pages/suplier/suplierList.js"
import { purchasePage } from "./pages/purchase/purchaseList.js"
import { productTemplatePage } from "./pages/productTemplate/productTemplateList.js"

export const routes = {
    "#/" : dashboardContent,
    "#/category" : categoryPage,
    "#/category/create" : categoryCreatePage,
    "#/subcategory" : subCategoryPage,
    "#/subcategory/create" : subCategoryCratePage,
    "#/brand" : brandPage,
    "#/customer" : customerPage,
    "#/user" : userPage,
    "#/suplier" : suplierPage,
    "#/purchase" : purchasePage,
    "#/product_template" : productTemplatePage
}
