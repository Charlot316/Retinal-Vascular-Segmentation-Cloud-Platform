import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    redirect: "/Login",
  },
  {
    path: "/register",
    name: "Register",
    component: () => import("../views/Register.vue"),
  },
  {
    path: "/login",
    name: "Login",
    component: () =>
      import(
        /* webpackChunkName: "login" */
        "../views/Login.vue"
      ),
  },
  {
    /* 患者的页面的路由*/
    path: "/patient",
    name: "Patient",
    children: [
      {
        path: "/user",
        name: "user",
        meta: {
          title: "个人中心",
          requireAuth: true,
          keepAlive: true,
        },
        component: () => import("../views/Patient/User.vue"),
      },
    ],
    component: () =>
      import(
        /* webpackChunkName: "login" */
        "../views/Patient/Home.vue"
      ),
  },
];

const router = createRouter({
  history: createWebHistory("/"),
  routes,
});

export default router;
