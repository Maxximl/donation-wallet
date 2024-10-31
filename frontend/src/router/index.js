import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/Login.vue';
import PostsList from '../components/PostsList.vue';
import OrganizationDetail from '../components/OrganizationDetail.vue'

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login,
  },
  {
    path: '/posts',
    name: 'PostsList',
    component: PostsList,
  },
  {
    path: '/organization/:id',
    name: 'OrganizationDetail',
    component: OrganizationDetail,
    props: true 
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
