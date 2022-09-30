import request from '@/utils/request'

// directly get whole list from DB
export function getAccessionList(listQuery) {
  return request({
    url: '/accessiondata/table/list/',
    method: 'post',
    data: listQuery
  })
}

// create new instance
export function createAccessionInfo(data) {
  return request({
    url: '/accessiondata/',
    method: 'post',
    data: data
  })
}

// getter
export function getAllAccessionInfo() {
  return request({
    url: '/accessiondata/',
    method: 'get'
  })
}

// getter by id
export function getAccessionInfoById(id) {
  return request({
    url: '/accessiondata/' + id,
    method: 'get'
  })
}

// update info
export function UpdateAccessionInfoById(data) {
  return request({
    url: '/accessiondata/' + data.id,
    method: 'put',
    data: data
  })
}

// delete by id
export function DeleteAccessionInfoById(id) {
  return request({
    url: '/accessiondata/' + id,
    method: 'delete'
  })
}
