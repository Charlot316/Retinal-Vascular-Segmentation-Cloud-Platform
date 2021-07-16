import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";

const routes = [
    {
        path: '/',
        redirect: '/search'
    }, {
        path: "/register",
        name: "Register",
        component: () => import("../views/Register.vue")
    },
    {
        path: "/login",
        name: "Login",
        component: () => import(
            /* webpackChunkName: "login" */
            "../views/Login.vue")
    }, {
        path: "/",
        name: "Home",
        component: Home,
        children: [
            {
                path: "/user",
                name: "user",
                meta: {
                    title: '个人中心',
                    requireAuth: true,
                    keepAlive: true
                },
                component: () => import("../views/User.vue")
            },
            {
                path: "/search",
                name: "search",
                meta: {
                    title: '搜索页面',
                    keepAlive: false
                },
                component: () => import(
                    /* webpackChunkName: "User" */
                    "../views/Search.vue")
            },
            {
                path: "/adminbook",
                name: "adminbook",
                meta: {
                    title: '管理图书',
                    keepAlive: false
                },
                component: () => import(
                    /* webpackChunkName: "User" */
                    "../views/AdminBook.vue")
            },
            {
                path: "/adminrb",
                name: "adminrb",
                meta: {
                    title: '借阅管理',
                    keepAlive: false
                },
                component: () => import(
                    /* webpackChunkName: "User" */
                    "../views/AdminRB.vue")
            },
            {
                path: "/adminuser",
                name: "adminuser",
                meta: {
                    title: '用户管理',
                    keepAlive: false
                },
                component: () => import(
                    /* webpackChunkName: "User" */
                    "../views/AdminUser.vue")
            },
            {
                path: "/popularbook",
                name: "popularbook",
                meta: {
                    title: '图书推荐',
                    keepAlive: false
                },
                component: () => import(
                    /* webpackChunkName: "User" */
                    "../views/PopularBook.vue")
            },
            {
                path: "/showReserveBook",
                name: "ShowReserveBook",
                meta: {
                    title: '已预约图书',
                    requireAuth: true,
                    keepAlive: false
                },
                component: () => import(
                    /* webpackChunkName: "User" */
                    "../views/ShowReserveBook.vue")
            },
            {
                path: "/showReturnedBook",
                name: "ShowReturnedBook",
                meta: {
                    title: '已归还图书',
                    requireAuth: true,
                    keepAlive: false
                },
                component: () => import("../views/ShowReturnedBook.vue")
            },
            {
                path: "/showTobeList",
                name: "ShowTobeList",
                meta: {
                    title: '在借图书',
                    requireAuth: true,
                    keepAlive: false
                },
                component: () => import("../views/ShowTobeList.vue")
            },
            {
                path: "/notification",
                name: "Notification",
                meta: {
                    title: '系统通知',
                    keepAlive: false
                },
                component: () => import("../views/Notification.vue")
            },
            {
                path: "/about",
                name: "About",
                meta: {
                    title: '关于本馆',
                    keepAlive: false
                },
                component: () => import("../views/About.vue")
            }
        ]
    },
];

const router = createRouter({
    history: createWebHistory('/'),
    routes
});


export default router;