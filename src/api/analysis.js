import request from '@/utils/request'

// directly get whole list from DB
export function getFeatureDim(listQuery) {
  return request({
    url: '/analysis/featuredim/',
    method: 'post',
    data: listQuery
  })
}

export function getCellFraction(collectionQuery) {
  return request({
    url: '/analysis/cellfraction/',
    method: 'post',
    data: collectionQuery
  })
}

export function getBulkViolin(analyzeQuery) {
  return request({
    url: '/analyze/violin/',
    method: 'post',
    data: analyzeQuery
  })
}
// get global sums of current AccessionData Table
export function getQuerySum(listQuery) {
  return request({
    url: '/analyze/sum',
    method: 'post',
    data: listQuery
  })
}

// create new instance
export function createAccessionInfo(data) {
  return request({
    url: '/analyze/',
    method: 'post',
    data: data
  })
}

// getter
export function getAllAccessionInfo() {
  return request({
    url: '/analyze/',
    method: 'get'
  })
}

// getter by id
export function getAccessionInfoById(id) {
  return request({
    url: '/analyze/' + id,
    method: 'get'
  })
}

// update info
export function UpdateAccessionInfoById(data) {
  return request({
    url: '/analyze/' + data.id,
    method: 'put',
    data: data
  })
}

// delete by id
export function DeleteAccessionInfoById(id) {
  return request({
    url: '/analyze/' + id,
    method: 'delete'
  })
}
