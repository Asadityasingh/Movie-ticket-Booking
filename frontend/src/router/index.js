import { createRouter, createWebHashHistory } from "vue-router";
import HomePage from "@/views/HomePage.vue";
import UserRegistration from "@/components/UserRegistration.vue";
// import LoginPage from "@/components/LoginPage.vue";
import AddTheatre from "@/components/AddTheatre.vue";
import AddShows from "@/components/AddShows.vue";
import AdminDashboard from "@/components/AdminDashboard.vue";
import ViewShows from "@/components/ViewShows.vue";
import EditShows from "@/components/EditShows.vue";
import EditTheatre from "@/components/EditTheatre.vue";
import LoginView from "@/views/LoginView.vue";
import SearchResult from "@/components/SearchResult.vue";

const routes = [
  {
    path: "/",
    name: "HomePage",
    component: HomePage,
  },
  {
    path: "/login",
    name: "LoginView",
    component: LoginView,
  },
  {
    path: "/register",
    name: "UserRegistration",
    component: UserRegistration,
  },
  // {
  //   path: "/login",
  //   name: "Login",
  //   component: LoginPage,
  // },
  {
    path: "/addtheatre",
    name: "AddTheatre",
    component: AddTheatre,
    meta: { requiresAuth: true },
  },
  {
    path: "/addshow/:id",
    name: "AddShows",
    component: AddShows,
    meta: { requiresAuth: true },
  },
  {
    path: '/admindashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true },
  },
  {
    path: "/viewshow/:id",
    name: "ViewShows",
    component: ViewShows,
    meta: { requiresAuth: true },
  },
  {
    path: "/eidtshow/:id",
    name: "EditShows",
    component: EditShows,
    meta: { requiresAuth: true },
  },
  {
    path: "/editTheatre/:id",
    name: "EditTheatre",
    component: EditTheatre,
    meta: { requiresAuth: true },
  },
  {
    path: '/search/:data',
    name: 'search',
    component: SearchResult,
    meta: { requiresAuth: true },
  }
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (localStorage.getItem("token") == null) {
      next({
        path: "/login",
        params: { nextUrl: to.fullPath },
      });
    } else {
      next();
    }
  } else {
    next();
  }
});


export default router;
