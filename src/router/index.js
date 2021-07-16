import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";

const routes = [
    {
        path: '/',
        redirect: '/Login'
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
        ]
    },
];

const router = createRouter({
    history: createWebHistory('/'),
    routes
});


export default router;