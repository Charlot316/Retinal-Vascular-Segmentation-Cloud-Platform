import { createRouter, createWebHistory } from "vue-router";

const routes = [
  /* 公共路由*/
  {
    /*用于指定初始界面的路由 */
    path: "/",
    redirect: "/login",
  },
  {
    path: "/register",
    name: "Register",
    component: () => import("../views/Public/Register"),
  },
  {
    path: "/login",
    name: "Login",
    component: () =>
      import(
        /* webpackChunkName: "login" */
        "../views/Public/Login"
      ),
  },
  /* 患者的页面的路由*/
  {
    path: "/patient",
    name: "Patient",
    children: [
      {
        path: "/patient/user",
        name: "/patient/user",
        meta: {
          title: "个人中心",
        },
        component: () => import("../views/Patient/User"),
      },
    ],
    component: () =>
      import(
        /* webpackChunkName: "login" */
        "../views/Patient/Home"
      ),
  },
  /* 医生的页面的路由*/
  {
    path: "/",
    name: "Doctor",
    children: [
      {
        path: "/doctor/user",
        name: "/doctor/user",
        meta: {
          title: "个人中心",
        },
        component: () => import("../views/Doctor/User"),
      },
    ],
    component: () =>
      import(
        /* webpackChunkName: "login" */
        "../views/Doctor/Home"
      ),
  },
  /* 管理员的页面的路由*/
  {
    path: "/",
    name: "Administrator",
    children: [
      {
        path: "/administrator/user",
        name: "user",
        meta: {
          title: "个人中心",
        },
        component: () => import("../views/Administrator/User"),
      },
    ],
    component: () =>
      import(
        /* webpackChunkName: "login" */
        "../views/Administrator/Home"
      ),
  },
];

const router = createRouter({
  history: createWebHistory("/"),
  routes,
});

export default router;
