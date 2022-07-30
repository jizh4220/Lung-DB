import request from '@/utils/request'

// create new instance
export function createAuthorInfo(data) {
  return request({
    url: '/author/',
    method: 'post',
    data: data
  })
}

// getter
export function getAuthorInfo() {
  return request({
    url: '/author/',
    method: 'get',
  })
}

// getter by id
export function getAuthorInfoById(id) {
  return request({
    url: '/author/' + id,
    method: 'get',
  })
}

// update info
export function UpdateAuthorInfoById(data) {
  return request({
    url: '/author/' + data.id,
    method: 'put',
    data: data
  })
}

// delete by id
export function DeleteAuthorInfoById(id) {
  return request({
    url: '/author/' + id,
    method: 'delete',
  })
}