import request from '@/utils/request'

export function findPage(page) {
  return request({
    url: '/post/page',
    method: 'post',
    data: page
  })
}
export function getById(id) {
  return request({
    url: '/post/getById/' + id,
    method: 'get'
  })
}
export function save(post) {
  return request({
    url: '/post/add',
    method: 'post',
    data: post
  })
}
export function updateById(post) {
  return request({
    url: '/post/updateById',
    method: 'put',
    data: post
  })
}
export function delById(id) {
  return request({
    url: '/post/del/' + id,
    method: 'delete'
  })
}
