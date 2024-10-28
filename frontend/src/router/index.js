import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/Login.vue';
import ResetPassword from '../components/ResetPassword.vue';
import PostsList from '../components/PostsList.vue';

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login,
  },
  {
    path: '/reset-password',
    name: 'ResetPassword',
    component: ResetPassword,
  },
  {
    path: '/posts',
    name: 'PostsList',
    component: PostsList,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
