// src/router.js
import { createRouter, createWebHistory } from 'vue-router';
import LoginView from './views/LoginView.vue';
import UserDashboard from './views/UserDashboard.vue';
import AdminDashboard from './views/AdminDashboard.vue';

const routes = [
  {
    path: '/',
    name: 'Login',
    component: LoginView
  },
  {
    path: '/usuario',
    name: 'Usuario',
    component: UserDashboard
  },
  {
    path: '/admin',
    name: 'Admin',
    component: AdminDashboard
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
