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
  {
    path: "/home",
    name: "Home",
    component: () =>
      import(
        /* webpackChunkName: "login" */
        "../views/Public/Home"
      ),
  },
  /* 患者的页面的路由*/
  {
    path: "/patient",
    name: "Patient",
    children: [
      {
        path: "user",
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
    path: "/doctor",
    name: "Doctor",
    children: [
      {
        path: "user",
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
    path: "/administrator",
    name: "Administrator",
    children: [
      {
        path: "user",
        name: "user",
        meta: {
          title: "个人中心",
        },
        component: () => import("../views/Administrator/User"),
      },
      {
        path: "admin/patient",
        name: "admin/patient",
        meta: {
          title: "患者管理",
        },
        component: () => import("../views/Administrator/Patient"),
      },
      {
        path: "admin/doctor",
        name: "admin/doctor",
        meta: {
          title: "医生管理",
        },
        component: () => import("../views/Administrator/Doctor"),
      },
      {
        path: "admin/drug",
        name: "admin/drug",
        meta: {
          title: "药品管理",
        },
        component: () => import("../views/Administrator/Drug"),
      },
      {
        path: "admin/operation",
        name: "admin/operation",
        meta: {
          title: "手术管理",
        },
        component: () => import("../views/Administrator/Operation"),
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
