import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },

  {
    path: '/',
    component: Layout,
    redirect: '/home',
    children: [{
      path: 'home',
      name: 'home',
      component: () => import('@/views/dashboard/index'),
      meta: { title: 'Front Page', icon: 'home' }
    }]
  },

  {
    path: '/example',
    component: Layout,
    redirect: '/example/table',
    name: 'Example',
    meta: { title: 'Example', icon: 'el-icon-s-help' },
    children: [
      {
        path: 'table',
        name: 'Table',
        component: () => import('@/views/table/index'),
        meta: { title: 'Table', icon: 'table' }
      },
      {
        path: 'tree',
        name: 'Tree',
        component: () => import('@/views/tree/index'),
        meta: { title: 'Tree', icon: 'tree' }
      }
    ]
  },

  {
    path: '/form',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'Form',
        component: () => import('@/views/form/index'),
        meta: { title: 'Form', icon: 'form' }
      }
    ]
  },

  /**
 {
    path: '/nested',
    component: Layout,
    redirect: '/nested/menu1',
    name: 'Nested',
    meta: {
      title: 'Nested',
      icon: 'nested'
    },
    children: [
      {
        path: 'menu1',
        component: () => import('@/views/nested/menu1/index'), // Parent router-view
        name: 'Menu1',
        meta: { title: 'Menu1' },
        children: [
          {
            path: 'menu1-1',
            component: () => import('@/views/nested/menu1/menu1-1'),
            name: 'Menu1-1',
            meta: { title: 'Menu1-1' }
          },
          {
            path: 'menu1-2',
            component: () => import('@/views/nested/menu1/menu1-2'),
            name: 'Menu1-2',
            meta: { title: 'Menu1-2' },
            children: [
              {
                path: 'menu1-2-1',
                component: () => import('@/views/nested/menu1/menu1-2/menu1-2-1'),
                name: 'Menu1-2-1',
                meta: { title: 'Menu1-2-1' }
              },
              {
                path: 'menu1-2-2',
                component: () => import('@/views/nested/menu1/menu1-2/menu1-2-2'),
                name: 'Menu1-2-2',
                meta: { title: 'Menu1-2-2' }
              }
            ]
          },
          {
            path: 'menu1-3',
            component: () => import('@/views/nested/menu1/menu1-3'),
            name: 'Menu1-3',
            meta: { title: 'Menu1-3' }
          }
        ]
      },
      {
        path: 'menu2',
        component: () => import('@/views/nested/menu2/index'),
        name: 'Menu2',
        meta: { title: 'menu2' }
      }
    ]
  },

  {
    path: 'external-link',
    component: Layout,
    children: [
      {
        path: 'https://panjiachen.github.io/vue-element-admin-site/#/',
        meta: { title: 'External Link', icon: 'link' }
      }
    ]
  },
 */
  
  {
    path: '/books',
    component: Layout,
    redirect: '/book/author',
    name: 'Book',
    meta: { title: 'Book Management', icon: 'el-icon-s-help' },
    children: [
      {
        path: 'author',
        name: 'author',
        component: () => import('@/views/author/index'),
        meta: { title: 'author information', icon: 'table' }
      },
      {
        path: 'book',
        name: 'book',
        component: () => import('@/views/book/index'),
        meta: { title: 'book information', icon: 'table' }
      },
    ]
  },

  {
    path: '/study',
    component: Layout,
    // redirect: '/book/author',
    name: 'study',
    meta: { title: 'Study Layout', icon: 'el-icon-s-help' },
    children: [
      {
        path: 'sample',
        name: 'sample',
        component: () => import('@/views/sample/index'),
        meta: { title: 'sample information', icon: 'table' }
      },
      {
        path: 'tissue',
        name: 'tissue',
        component: () => import('@/views/tissue/index'),
        meta: { title: 'tissue layout', icon: 'table' }
      },
      {
        path: 'disease',
        name: 'disease',
        component: () => import('@/views/disease/index'),
        meta: { title: 'disease layout', icon: 'table' }
      },
      {
        path: 'gender',
        name: 'gender',
        component: () => import('@/views/gender/index'),
        meta: { title: 'gender layout', icon: 'table' }
      },
      {
        path: 'age',
        name: 'age',
        component: () => import('@/views/age/index'),
        meta: { title: 'age layout', icon: 'table' }
      },
      {
        path: 'metadata',
        name: 'metadata',
        component: () => import('@/views/metadata/index'),
        meta: { title: 'metadata layout', icon: 'table' }
      },
    ]
  },

  {
    path: '/post',
    component: Layout,
    redirect: '/post',
    children: [{
      path: 'post',
      name: 'Post',
      component: () => import('@/views/post/list'),
      meta: { title: 'Jobs Management', icon: 'el-icon-menu' }
    }]
  },

  {
    path: '/test',  
    component: Layout, 
    children: [{
      path: 'test', 
      name: 'test',
      component: () => import('@/views/test/index'),
      meta: {
        title: 'test', icon:'plane'
      }
    }]
  },

  {
    path: 'customize',
    name: 'Customize',
    component: () => import('@/views/customize/index'),
    meta: { title: 'Customization', icon: 'table' }
  },

  {
    path: 'wordcloud',
    name: 'wordcloud',
    component: () => import('@/views/wordcloud/index'),
    meta: { title: 'WordCloud', icon: 'table' }
  }

  /**
  {
    path: '/material',
    component: Layout,
    redirect: '/material/upload',
    meta: {
      title: 'Element Management System',
      icon: 'plane' 
    },
    children: [{
        path: 'check-template',
        name: 'check-template',
        component: () => import('@/views/material/check-template'),
        meta: {
          title: 'Check Template',
        }
      },
      {
        path: 'logo',
        name: 'logo',
        component: () => import('@/views/material/check-logo'),
        meta: {
          title: 'Check Logo',
        }
      },
      {
        path: 'generate',
        name: 'generate',
        component: () => import('@/views/material/generate'),
        meta: {
          title: 'Generate Element',
        }
      },
      {
        path: 'check',
        name: 'check',
        component: () => import('@/views/material/check'),
        meta: {
          title: 'Check Element',
        }
      },
    ]
  },
  */

  // 404 page must be placed at the end !!!
  // { path: '*', redirect: '/404', hidden: true }
]

export const asyncRoutes = [
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  mode: 'hash', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
